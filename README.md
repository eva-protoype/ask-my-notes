# Ask My Notes

A multi-subject RAG app for asking questions about my college notes. PDFs are ingested into a separate Chroma collection for each subject, and a FastAPI backend routes questions to that subject's notes. Gemini generates answers from retrieved chunks, with page citations.

Built by Tanishq Singh for exam prep and as a student portfolio project.

**Status:** PDF ingestion, per-subject storage, retrieval, and the FastAPI endpoints are implemented. The Streamlit frontend, Docker setup, and deployment are next.

This is a single-user app. Subject collections keep different sets of notes separate; they are not user accounts or access controls.

## Stack

- Python 3.12
- FastAPI and Pydantic
- pypdf for PDF text extraction
- ChromaDB with `PersistentClient` for local storage
- Google Gemini through `google-genai` for embeddings and answers
- python-dotenv for loading environment variables

The current code uses `gemini-embedding-2` for embeddings and `gemini-3.5-flash-lite` for answer generation. Your Gemini API key needs access to both models.

## Setup

Clone the repository:

```bash
git clone https://github.com/eva-protoype/ask-my-notes.git
cd ask-my-notes
```

Create and activate a conda environment:

```bash
conda create -n ask-my-notes python=3.12 -y
conda activate ask-my-notes
```

If you already have a Python 3.12 conda environment, activate that instead.

Install the dependencies inside the active environment:

```bash
pip install "fastapi[standard]"
pip install pypdf chromadb google-genai python-dotenv
```

Create a `.env` file in the repository root:

```dotenv
GEMINI_API_KEY=your_api_key_here
```

Keep the key out of source control. The repository's `.gitignore` excludes `.env`, PDFs, and the `chroma/` data directory.

## Ingest a PDF

PDF ingestion currently runs through the Python functions, not an upload endpoint. From the repository root, replace `your_notes.pdf` with a text-based PDF's path:

```bash
python - <<'PY'
from extractor import pdf_pages, chunk_pages
from store import build_store

subject = "OS"
pages = pdf_pages("your_notes.pdf")
chunks = chunk_pages(pages)

if not chunks:
    raise SystemExit("No text chunks found. Use a PDF with a text layer.")

notes = build_store(chunks, subject)
print(f"{subject}: {notes.count()} stored chunks")
PY
```

Use uppercase subject names during ingestion, such as `OS` or `DBMS`. The API uppercases the incoming `sub` value, but `build_store()` does not normalize subject names. Ingesting under `os` and asking through the API would target different collections.

`get_collection(subject)` adds the `notes-` prefix internally:

```text
OS   -> notes-OS
DBMS -> notes-DBMS
```

Pass `OS`, not `notes-OS`, to the ingestion function or API. Use simple subject names with letters, numbers, underscores, or hyphens.

Chroma uses `PersistentClient()` without an explicit path. Run ingestion and the API from the same repository directory so they use the same local store.

Ingestion appends chunks. Running the same PDF through `build_store()` again duplicates its content; it does not replace the previous version.

## Run the API

From the repository root, with the conda environment active:

```bash
fastapi dev api.py
```

The development server normally runs at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for the interactive API docs.

### List subjects

```bash
curl http://127.0.0.1:8000/subjects
```

`GET /subjects` returns a JSON array of collection names with the `notes-` prefix removed. For example, after ingesting OS and DBMS notes:

```json
["OS", "DBMS"]
```

### Ask a question

```bash
curl -X POST http://127.0.0.1:8000/ask/ \
  -H 'Content-Type: application/json' \
  -d '{"query": "What is the convoy effect?", "sub": "OS"}'
```

The request body uses `query` and `sub`:

```json
{
  "query": "What is the convoy effect?",
  "sub": "OS"
}
```

`POST /ask/` returns the answer as a JSON string, not an object with separate `answer` and `sources` fields. Page citations are part of the generated answer text.

You can also use **Try it out** in `/docs`. Ingest notes for the chosen subject before asking questions.

## How it works

```text
PDF -> page text -> per-page chunks -> Gemini embeddings
                                          |
                                  notes-<subject> in Chroma
                                          |
Question + subject -> question embedding -> top 3 chunks
                                          |
                              Gemini answer with page citations
```

1. `pdf_pages()` extracts text with PDF page numbers starting at 1.
2. `chunk_pages()` splits each page into chunks of up to 400 words. Chunks never cross page boundaries.
3. `build_store()` embeds the chunks and stores their text, vectors, and page metadata in the subject's collection.
4. `doc_retrieval()` embeds the question using the same embedding model and retrieves three chunks by default.
5. `ask()` formats the retrieved context as `[page:N]` passages and asks Gemini to answer only from that context, cite every claim, and say it doesn't know when the context lacks the answer.
6. `api.py` exposes the question flow and subject list through FastAPI.

## File map

| File | Role |
| --- | --- |
| `extractor.py` | `pdf_pages()` and `chunk_pages()` for PDF extraction and chunking. |
| `store.py` | Gemini embeddings, subject collections, ingestion, and `list_subjects()`. |
| `retrieval.py` | Retrieves relevant chunks from the selected subject. |
| `ask.py` | Builds the context and prompt, calls Gemini, and returns answer text. |
| `api.py` | Pydantic request model, `POST /ask/`, and `GET /subjects`. |

## Current limits

- No OCR: pages without extractable text are skipped.
- No authentication or user-level separation. Keep the development API local.
- No PDF upload endpoint or frontend yet.
- Unknown subjects are not explicitly rejected: the collection helper can create an empty collection. Use subjects that have already been ingested.
- Chunk IDs are based on the collection count. Deleting chunks can cause ID collisions during later ingestion; PDF replacement is not implemented.
- Citations contain page numbers but no source filename, so multiple PDFs in one subject can have ambiguous page references.
- Retrieval and generated answers can be wrong. The citation prompt is a check against hallucination, not a guarantee. Verify answers against the notes.
- Gemini API access, quotas, and model availability affect both ingestion and questions.

## Roadmap

- [x] PDF extraction and per-page chunking
- [x] Gemini embeddings and persistent Chroma storage
- [x] Separate collections per subject
- [x] Retrieval and answers with page citations
- [x] FastAPI question and subject-list endpoints
- [ ] Streamlit frontend with a subject picker and chat interface
- [ ] Docker setup for the backend and frontend
- [ ] Deployment with persistent storage and environment-based secrets
