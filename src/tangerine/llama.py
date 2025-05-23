import os
import json
import uuid

from pathlib import Path
from typing import Generator, Any
from flask import Response, stream_with_context
from llama_stack_client import Agent, AgentEventLogger, RAGDocument
from llama_stack import LlamaStackAsLibraryClient

from .file import File
from .models.assistant import Assistant

class LlamaClient:
    def __init__(self):
        config_file = self._get_config_file()
        client = LlamaStackAsLibraryClient(config_file)
        client.initialize()

        vector_providers = [
            provider for provider in client.providers.list() if provider.api == "vector_io"
        ]
        self.provider_id = vector_providers[0].provider_id
        self.client = client

    def insert_documents(self, files: list[File], assistant: Assistant) -> None:
        documents = [
            RAGDocument(
                document_id=f"num-{uuid.uuid4()}",
                content=file.content,
                metadata=file.metadata
            )
            for i, file in enumerate(files)
        ]
        self.client.tool_runtime.rag_tool.insert(
            documents=documents,
            vector_db_id=f"assistant_{assistant.id}",
            chunk_size_in_tokens=1500,
        )

    def ask(
        self, assistant, question, interaction_id
    ):
        agent = self._create_agent(assistant)
        response = agent.create_turn(
            messages=[{"role": "user", "content": question}],
            session_id=agent.create_session(interaction_id),
            stream=True,
        )
        return response

    def register_assistant_vector(self, assistant: Assistant):
        self.client.vector_dbs.register(
            vector_db_id=f"assistant_{assistant.id}",
            provider_id=self.provider_id,
            embedding_model="nomic-embed-text:latest",
            embedding_dimension=768,
        )

    def unregister_assistant_vector(self, assistant: Assistant):
        self.client.vector_dbs.unregister(vector_db_id=assistant.id)

    @staticmethod
    def generate_response(response) -> Response:
        def build_stream() -> Generator[Any, Any, None]:
            for log in AgentEventLogger().log(response):
                log.print()
                content = log.content
                message = {
                    "text_content": str(content)
                }
                sse_line = f"data: {json.dumps(message)}\r\n"
                yield sse_line.encode("utf-8")
        return Response(stream_with_context(build_stream()))

    def _create_agent(self, assistant: Assistant) -> Agent:
        return Agent(
            self.client,
            model=os.environ["INFERENCE_MODEL"],
            instructions=assistant.system_prompt,
            enable_session_persistence=False,
            tools=[
                {
                    "name": "builtin::rag/knowledge_search",
                    "args": {
                        "vector_db_ids": [f"assistant_{assistant.id}"],
                    },
                }
            ],
        )

    def _get_config_file(self):
        project_root = Path(__file__).resolve()
        while not (project_root / "custom-template.yaml").exists():
            project_root = project_root.parent
        config_file = project_root / "custom-template.yaml"
        return str(config_file)

llama_client = LlamaClient()