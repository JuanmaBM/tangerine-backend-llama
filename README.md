# 🍊 Tangerine on Llama Stack (Backend) <!-- omit from toc -->

This project is a proof of concept (PoC) that demonstrates how to build a RAG (Retrieval-Augmented Generation) application similar to [Tangerine](https://github.com/RedHatInsights/tangerine-backend) using [Llama Stack](https://llama-stack.readthedocs.io/).

> ⚠️ **Disclaimer**: This project is not intended to replace Tangerine or serve as an updated fork. If you're interested in Tangerine features and updates, please refer to the official [Tangerine Backend Repository](https://github.com/RedHatInsights/tangerine-backend)

---

## 📦 Prerequisites

- Python 3.12
- Pipenv
- [Ollama](https://ollama.com/)
- Docker or Podman  
  _(You may use your own PostgreSQL instance, but ensure it matches the configuration in the `postgresql/` folder.)_

---

## 🚀 Installation Guide

### ✅ Install Pipenv

```bash
pip install pipenv
pipenv --version
```

### 🧠 Install Ollama

1. Visit [ollama.com](https://ollama.com/)
2. Download and run the installer for your OS.
3. Verify installation:

    ```bash
    ollama --version
    ```

4. Pull and run a model:

    ```bash
    ollama run llama3.2:3b-instruct-fp16 --keepalive 1m
    ```

5. Type `/bye` to exit the prompt.

---

## 🛠️ Getting Started

### 📁 Set Up the Virtual Environment

```bash
pipenv install --dev
pipenv shell
```

### 🐘 Start PostgreSQL with Podman

Navigate to the `postgresql/` folder and run:

```bash
podman run --name customvector \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -v $(pwd)/01-init-users.sql:/docker-entrypoint-initdb.d/01-init-users.sql:Z \
  -v $(pwd)/02-init-db.sql:/docker-entrypoint-initdb.d/02-init-db.sql:Z \
  -v $(pwd)/03-extensions.sql:/docker-entrypoint-initdb.d/03-extensions.sql:Z \
  -p 5432:5432 \
  -d pgvector/pgvector:pg17
```

---

## 🔧 Environment Variables

Set these variables in your shell or in the `launch.json` file (if using VS Code):

- `INFERENCE_MODEL`: The model used for inference (must be available on your model server).
- `LLAMA_STACK_PORT`: Port on which the Llama Stack server is running (e.g., `8321`).

---

## 🧪 Running the Application

### ▶️ From Terminal

```bash
flask run
```

### 🐞 From Visual Studio Code

1. Make sure environment variables are defined under `env` in your launch config.
2. Run the debug task named `Debug tangerine backend`.

---

## ⚙️ Llama Stack Distribution Configuration

This project uses `custom-template.yaml` to define the Llama Stack setup.

By default, it configures:
- **PostgreSQL** as the vector database.
- **Ollama** as the inference provider.

### 🧩 Optional: Add a Remote Inference Provider

To use a remote VLLM instance, uncomment and complete the following in `custom-template.yaml`:

```yaml
inference:
  - config:
      url: https://llama-scout-maas.com/v1
      api_token: 123456789123456789
    provider_id: vllm-inference
    provider_type: remote::vllm
```

And register the model:

```yaml
models:
  - metadata: {}
    model_id: llama-scout-maas
    provider_id: vllm-inference
    provider_model_id: null
```
