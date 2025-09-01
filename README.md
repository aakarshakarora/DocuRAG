# 📘 DocuRAG

DocuRAG is a **Retrieval-Augmented Generation (RAG)** assistant for exploring documentation.  
You can feed it any set of documentation (`.html`, `.md`, `.txt`) and query it interactively using a local LLM via *
*Ollama**.  
It will only answer based on the ingested docs, otherwise respond with:

```
Not covered in the documentation.
```

---

## 🔑 Features

- Ingest `.html`, `.md`, and `.txt` documentation into a vector database (ChromaDB).
- Query the docs interactively using an LLM (local Ollama model).
- Enforces strict grounding in the ingested docs.
- Works offline after setup.

---

## ⚙️ Prerequisites

### 🐍 Python

- Python **3.10+**
- Virtual environment (`venv`)

### 📦 System Packages

- On Linux/macOS: `make`, `python3-venv`
- On Windows: use Git Bash or WSL for Makefile support

### 🧠 Ollama

Ollama runs LLMs locally on your machine. Install Ollama:

**macOS:**

```bash
brew install ollama
```

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows (Preview):**
Download from [Ollama Releases](https://ollama.com/download).

---

## 📥 Install Ollama Models

DocuRAG is lightweight by default and uses the **Phi-3 Mini** model (~1.5GB).

```bash
ollama pull phi3:mini
```

Optional (larger models):

```bash
ollama pull llama3
ollama pull mistral
```

---

## 🚀 Setup & Usage

1. **Clone the repo**:
   ```bash
   git clone https://github.com/aakarshakarora/DocuRAG.git
   cd DocuRAG
   ```

2. **Prepare virtual environment**:
   ```bash
   make prepare-venv
   ```
   
3.	**Configure Documentation Collections**:

   Place documentation inside data/:

   ```   data/
      ├── python_docs/     # example: extracted Python docs
      ├── java_docs/       # example: extracted Java docs
   ```
   Use settings.json to define one or more documentation collections:

   ```{
        "docs": [
          {
            "name": "python315",
            "path": "./data/python-3.15-docs-html"
          },
          {
            "name": "java11",
            "path": "./data/java-11-docs-html"
          }
        ]
      }
   ```
   name → unique collection name 
   path → folder containing the documentation files (.html, .md, .txt)

4. **Ingest docs**:
   ```bash
   make ingest
   ```
   You will be asked to confirm whether you’ve placed the docs correctly.

5. **Start interactive chat**:
   ```bash
   make chat
   ```

   Example:
   ```
   📘 Documentation Assistant (type 'stop' to quit)

   >>> How do I install Python packages?
   --- Answer ---
   Use pip to install additional modules...
   ```

6. **Format code (optional)**:
   ```bash
   make format
   ```

7. **Clean up (reset everything)**:
   ```bash
   make clean
   ```

---

## 📚 Example: Downloading Python Docs

To try DocuRAG with Python documentation:

```bash
# Download Python 3.15 docs
curl -O https://docs.python.org/3.15/archives/python-3.15-docs-html.tar.bz2

# Extract into data folder
mkdir -p data/python_docs
tar -xvjf python-3.15-docs-html.tar.bz2 -C data/python_docs
```

Then run:

```bash
make ingest
make chat
```

---

## 🛠 Requirements

All dependencies are listed in `requirements.txt`. They are installed automatically via:

```bash
make prepare-venv
```

Key dependencies:

- `chromadb`
- `sentence-transformers`
- `beautifulsoup4`
- `typer`
- `ollama-python`

---

## ✨ Future Enhancements

- Multi-doc querying (choose between `python_docs`, `java_docs`, etc.)
- Web UI with chat history
- Dockerized deployment

---

📌 **DocuRAG** = Documentation + RAG → Focused, grounded answers.