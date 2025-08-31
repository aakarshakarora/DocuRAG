import typer
from utils.ingest import ingest
from utils.rag import query_docs
from utils.config import collections

app = typer.Typer()

@app.command()
def load():
    """Ingest documents into the vector DB."""
    ingest()

@app.command()
def chat():
    """Interactive Q&A with your docs (type 'stop' to quit)."""
    print("📘 Documentation Assistant (type 'stop' to quit)")

    # Let user select collection
    collection_names = list(collections.keys())
    print(f"Available doc collections: {', '.join(collection_names)}")
    collection_name = input(f"Which collection do you want to query? [{collection_names[0]}]: ").strip()
    if collection_name not in collections:
        collection_name = collection_names[0]  # default

    while True:
        question = input("\n>>> ")
        if question.lower().strip() in ["stop", "quit", "exit"]:
            print("👋 Goodbye!")
            break

        answer = query_docs(question, collection_name=collection_name)
        print("\n--- Answer ---\n" + answer)


if __name__ == "__main__":
    app()