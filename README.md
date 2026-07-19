# Intel Assist

**Intel Assist** is a local AI knowledge assistant for organisations that need to find answers across large collections of files. It turns documents into a searchable knowledge base, retrieves the most relevant passages for a question, and uses a local language model to produce a grounded answer with its source chunks.

It is intended for any organisation with substantial documentation to manage. Teams in schools, NGOs, clinics, agencies, professional services firms, startups, public bodies, and community organisations can use the same approach to make policies, procedures, project notes, manuals, and internal reference material easier to use.

## What it does today

- Accepts **TXT** and text-based **PDF** documents.
- Splits documents into readable chunks and embeds them with `all-MiniLM-L6-v2`.
- Stores embeddings in a local **FAISS** vector index for semantic search.
- Avoids adding duplicate chunks when documents are indexed again.
- Retrieves the top matching chunks for a user question.
- Sends the retrieved context to a local **Mistral** model via Ollama and instructs it to answer only from that context.
- Shows the answer and the chunks/documents used as sources.
- Provides three ways to use the prototype:
  - command-line workflow;
  - Streamlit web interface;
  - CustomTkinter desktop interface.
- Includes a small evaluation script with sample policy and project-document questions.

## How it works

```text
Documents (TXT / PDF)
        |
        v
Extract text -> chunk text -> create embeddings -> FAISS index
                                                |
Question -> embed question -> retrieve best chunks
                                                |
                                                v
                           Local Mistral model generates an answer
                                                |
                                                v
                                Answer + supporting source chunks
```

This pattern is commonly called retrieval-augmented generation (RAG). Rather than asking the model to rely on general memory, Intel Assist supplies relevant content from the indexed files at question time.

## Project structure

```text
intelAssist/
├── data/
│   ├── docs/               # Sample/source documents for command-line indexing
│   ├── vector.index        # Generated FAISS index
│   └── chunks.pkl          # Generated chunk metadata
├── src/
│   ├── ingest.py           # TXT/PDF reading and text chunking
│   ├── embed_store.py      # Embeddings, deduplication, and FAISS persistence
│   ├── retrieve.py         # Semantic retrieval
│   ├── llm.py              # Local Ollama/Mistral request
│   ├── main.py             # Command-line application
│   ├── web_app.py          # Streamlit interface
│   ├── desktop_app.py      # CustomTkinter desktop interface
│   └── evaluate.py         # Sample retrieval/answer evaluation
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or later is recommended.
- [Ollama](https://ollama.com/) installed and running locally.
- The Mistral model available to Ollama:

  ```powershell
  ollama pull mistral
  ```

The application currently calls `http://localhost:11434/api/generate` and uses the model name `mistral`. Change `src/llm.py` if your local Ollama host or model name is different.

## Installation

From the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama serve
```

Keep `ollama serve` running in a separate terminal if it is not already running as a background service.

## Use Intel Assist

### Option 1: Web interface

```powershell
streamlit run src/web_app.py
```

The browser app indexes files already in `data/docs/` when no index exists. You can also upload TXT and PDF files directly in the page, then ask questions and inspect the retrieved sources.

### Option 2: Desktop interface

```powershell
python src/desktop_app.py
```

Use **Upload Documents** to add TXT or PDF files. Enter a question and select the **Sources / Chunks** tab to see the evidence retrieved for the answer.

### Option 3: Command line

Place files in `data/docs/`, then run:

```powershell
python src/main.py
```

The command-line flow indexes the folder, asks for one question, prints the answer, and displays the retrieved records.

### Evaluate the sample data

```powershell
python src/evaluate.py
```

This runs the included sample questions and reports basic retrieval and keyword-based answer scores. It is a development check, not a benchmark of real-world accuracy.

## Data and privacy

The current prototype is designed to run locally:

- embeddings and indexed chunk metadata are stored under `data/`;
- generation is requested from a local Ollama endpoint;
- uploaded files are processed into the local persistent index.

Before using sensitive records, review the local machine’s access controls, backups, and the model/runtime configuration. The current index is shared by the application instance; it does not yet enforce per-user or per-team permissions.

## Current limitations

This is an early working prototype. In particular:

- Only TXT and text-extractable PDFs are supported; scanned PDFs need OCR first.
- The vector index uses a simple flat FAISS L2 index and has no document deletion, filtering, versioning, or collection separation.
- Source information currently identifies files and chunks, not page numbers or detailed citations.
- Retrieval and generation have limited error handling, guardrails, and observability.
- No authentication, role-based access control, audit trail, or multi-user workspace is implemented.
- The quality of answers depends on document extraction, chunking, retrieval, and the local model. Users should verify important answers against the displayed source material.

## Product goal

Intel Assist aims to become a dependable file-intelligence workspace for organisations that are overwhelmed by documents. The end goal is to let people securely ask natural-language questions across their authorised organisational knowledge and receive useful, traceable answers—without needing to remember which folder, file, or version contains the information.

Planned areas of growth include:

- broader file support, including Word, spreadsheets, presentations, scanned documents, and images with OCR;
- robust document collections, metadata, deletion, versioning, and re-indexing;
- citations with file, page, and passage links;
- secure user accounts, teams, role-based access, and audit history;
- connectors for shared drives and document platforms;
- better retrieval, reranking, multilingual support, and feedback-driven evaluation;
- organisation-level deployment, administration, and monitoring.

## Technology used

- Python
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- PyPDF
- Ollama with Mistral
- Streamlit
- CustomTkinter

## License

This project is licensed under the [MIT License](LICENSE).
