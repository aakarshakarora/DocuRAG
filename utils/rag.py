import ollama
from utils.config import collections, embedder, SYSTEM_PROMPT

def query_docs(question: str, collection_name: str, model: str = "phi3:mini") -> str:
    """Query docs with a question and return an answer from LLM."""

    if collection_name not in collections:
        return f"Collection '{collection_name}' not found."

    collection = collections[collection_name]

    # embed query
    query_emb = embedder.encode(question).tolist()

    # query vector DB
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=5,
        include=["distances", "documents"]
    )

    distances = results["distances"][0]
    docs = [doc for doc, dist in zip(results["documents"][0], distances) if dist < 1.2]

    if not docs and results["documents"]:
        docs = results["documents"][0][:2]

    context = "\n\n".join(docs) if docs else ""

    if not context.strip():
        return "Not covered in the docs."

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Docs:\n{context}\n\nQuestion: {question}"}
        ]
    )

    return response["message"]["content"]