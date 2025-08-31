import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load settings
with open("settings.json", "r", encoding="utf-8") as f:
    DOCS_SETTINGS = json.load(f).get("docs", [])

# Initialize ChromaDB collections
chroma_client_dict = {}
collections = {}

for doc in DOCS_SETTINGS:
    name = doc["name"]
    path = doc["path"]
    client = chromadb.PersistentClient(path=f"./db/{name}_db")
    coll = client.get_or_create_collection(name)
    chroma_client_dict[name] = client
    collections[name] = coll

# Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# System prompt
SYSTEM_PROMPT = """
You are a Documentation Assistant.
Only answer using the provided documentation.
If the answer is not in the provided docs, say:
'Not covered in the docs.'
"""