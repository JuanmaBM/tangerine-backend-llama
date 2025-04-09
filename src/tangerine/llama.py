import os
import uuid
from llama_stack_client import Agent, AgentEventLogger, RAGDocument
from llama_stack import LlamaStackAsLibraryClient

from .file import File, validate_file_path, validate_source
from .models.assistant import Assistant

class LlamaClient:
    def __init__(self):
        client = LlamaStackAsLibraryClient("ollama")
        client.initialize()

        vector_providers = [
            provider for provider in client.providers.list() if provider.api == "vector_io"
        ]
        provider_id = vector_providers[0].provider_id
        self.vector_db_id = "tangerine-vector-db"
        client.vector_dbs.register(
            vector_db_id=self.vector_db_id,
            provider_id=provider_id,
            embedding_model="all-MiniLM-L6-v2",
            embedding_dimension=384,
        )

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
            vector_db_id=self.vector_db_id,
            chunk_size_in_tokens=512,
        )

    def ask(
        self, assistant, question, interaction_id
    ):
        agent = self._create_agent()
        response = agent.create_turn(
            messages=[{"role": "user", "content": question}],
            session_id=agent.create_session(interaction_id),
            stream=True,
        )
        # for log in AgentEventLogger().log(response):
        #     log.print()
        return response

    def _create_agent(self) -> Agent:
        return Agent(
            self.client,
            model=os.environ["INFERENCE_MODEL"],
            instructions="You are a helpful assistant. Use the knowledge_search tool to get information. You must not ask something that is not in your knowledge_search information",
            enable_session_persistence=False,
            tools=[
                {
                    "name": "builtin::rag/knowledge_search",
                    "args": {
                        "vector_db_ids": [self.vector_db_id],
                    },
                }
            ],
        )

llama_client = LlamaClient()