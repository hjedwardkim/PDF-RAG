# RAG Prototype Application

This project implements a RAG prototype using FastAPI, PostgreSQL with pgvector, and Azure OpenAI.

## Prerequisites
- Docker
- Docker Compose
- Python 3.9+

## Setup
1. Clone the repository:
   ```
   git clone https://github.com/your-username/rag-prototype.git
   cd rag-prototype
   ```

2. Create a `.env` file in the root directory with the following content:
   ```
   AZURE_OPENAI_KEY=your_azure_openai_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment
   AZURE_OPENAI_LLM_DEPLOYMENT=your_llm_deployment
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_postgres_db
   ```

3. Build and run the containers:
   ```
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000`.

## Usage
You can interact with the RAG Prototype in several ways:

### 1. Web Interface
Open `http://localhost:8000` in your web browser to access the simple web interface. Here you can:
- Upload documents
- Ask questions about the uploaded documents
### 2. Command-Line Interface (CLI)
The `query_cli.py` script provides a command-line interface for interacting with the RAG system.

First, ensure you have the required dependencies:

```bash
pip install typer requests
```

Then you can use the CLI as follows:

- Upsert a document:
  ```
  python query_cli.py upsert /path/to/your/document.pdf
  ```

- Search documents:
  ```
  python query_cli.py query "What is the main topic of the document?"
  ```

- Start an interactive session:
  ```
  python query_cli.py interactive
  ```

### 3. API Endpoints

You can also interact with the RAG system directly through its API endpoints:

- Upsert a document:
  ```
  curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/api/upsert
  ```

- Search documents:
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the main topic of the document?"}' http://localhost:8000/api/query
  ```

- Get document count:
  ```
  curl http://localhost:8000/api/document_count
  ```

- Get document filenames:
  ```
  curl http://localhost:8000/api/document_filenames
  ```

