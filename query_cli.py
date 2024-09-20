from pathlib import Path

import requests
import typer

app = typer.Typer()

BASE_URL = "http://localhost:8000/api"


def upsert_document(file_path: Path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upsert", files=files)
    typer.echo(response.json())


def query_documents(question: str):
    response = requests.post(f"{BASE_URL}/query", json={"question": question})
    result = response.json()
    typer.echo(f"Answer: {result['answer']}\n")


@app.command()
def upsert(file_path: Path = typer.Argument(..., help="Path to the file to upsert")):
    """Upsert a document to the RAG system."""
    upsert_document(file_path)


@app.command()
def query(question: str = typer.Argument(..., help="Question to ask")):
    """Query documents in the RAG system."""
    query_documents(question)


@app.command()
def interactive():
    """Start an interactive session to upsert documents and ask questions."""
    while True:
        action = typer.prompt("What would you like to do? (upsert/query/quit)")
        if action.lower() == "quit":
            break
        elif action.lower() == "upsert":
            file_path = typer.prompt("Enter the path to the file you want to upsert")
            upsert_document(Path(file_path))
        elif action.lower() == "query":
            question = typer.prompt("Enter your question")
            query_documents(question)
        else:
            typer.echo("Invalid action. Please choose upsert, query, or quit.")


if __name__ == "__main__":
    app()
