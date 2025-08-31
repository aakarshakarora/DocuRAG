import glob
import os
from bs4 import BeautifulSoup
from utils.config import DOCS_SETTINGS, embedder, collections


def ingest():
    total_chunks = 0

    for doc in DOCS_SETTINGS:
        name = doc["name"]
        path = doc["path"]
        abs_path = os.path.abspath(path)
        print(f"Looking in: {abs_path}")

        collection = collections[name]

        files = glob.glob(f"{path}/**/*", recursive=True)
        supported_ext = (".html", ".txt", ".md")
        doc_chunks = 0

        for filepath in files:
            if not filepath.endswith(supported_ext):
                continue

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()

            if filepath.endswith(".html"):
                soup = BeautifulSoup(raw, "html.parser")
                text = soup.get_text(strip=True)
            else:
                text = raw

            chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]

            for idx, chunk in enumerate(chunks):
                emb = embedder.encode(chunk).tolist()
                doc_id = f"{filepath}-{idx}"
                collection.add(documents=[chunk], embeddings=[emb], ids=[doc_id])

            doc_chunks += len(chunks)

        print(f"✅ Ingested {doc_chunks} chunks into collection '{name}'")
        total_chunks += doc_chunks

    print(f"🎉 Total chunks ingested across all collections: {total_chunks}")
