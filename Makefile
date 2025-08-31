# Python executable inside venv
VENV := .venv
ifeq ($(OS),Windows_NT)
    PYTHON_EXEC := $(VENV)/Scripts/python.exe
    PIP := $(VENV)/Scripts/pip.exe
    ACTIVATE := $(VENV)/Scripts/activate
    PYTHON := python
else
    PYTHON_EXEC := $(VENV)/bin/python
    PIP := $(VENV)/bin/pip
    ACTIVATE := $(VENV)/bin/activate
    PYTHON := python3
endif

DOCS_DIR := data/

.PHONY: prepare-venv ingest chat format clean

prepare-venv:
	@echo "🐍 Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✅ Virtual environment ready."

ingest:
	@if [ -d "$(DOCS_DIR)" ]; then \
		if find $(DOCS_DIR) -type f \( -name "*.html" -o -name "*.md" -o -name "*.txt" \) | grep -q .; then \
			echo "📂 Docs root folder found at $(DOCS_DIR)."; \
			read -p "👉 Have you placed your documentation inside subfolders of '$(DOCS_DIR)' (y/n)? " ans; \
			if [ "$$ans" = "y" ] || [ "$$ans" = "Y" ]; then \
				echo "✅ Found documentation files. Starting ingestion..."; \
				$(PYTHON_EXEC) main.py load; \
			else \
				echo "❌ Please add documentation inside $(DOCS_DIR)/<your_docs_folder>/"; \
				exit 1; \
			fi \
		else \
			echo "❌ No .html, .md, or .txt files found in $(DOCS_DIR)."; \
			exit 1; \
		fi \
	else \
		echo "❌ Docs directory '$(DOCS_DIR)' not found."; \
		exit 1; \
	fi

chat:
	@echo "💬 Starting chat..."
	@$(PYTHON_EXEC) main.py chat

format:
	@echo "✨ Formatting code..."
	@$(VENV)/bin/isort . || $(VENV)/Scripts/isort.exe .
	@$(VENV)/bin/black . || $(VENV)/Scripts/black.exe .

clean:
	@echo "🧹 Cleaning project..."
	rm -rf __pycache__ */__pycache__ .pytest_cache
	rm -rf chroma_db $(VENV)