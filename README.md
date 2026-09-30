# Ask My Notes

A RAG (retrieval-augmented generation) app for asking questions about my own college notes. Give it a PDF, build a local vector store, and ask questions in the terminal. Answers cite the pages used, so I can check them against the notes.

Built for my own exam prep first, and as a portfolio project for GenAI/ML internship applications.

> **Status: working terminal version.** PDF extraction, chunking, embeddings, retrieval, and the ask-question loop are in place. A Streamlit UI is next.

## The idea

Before exams I end up digging through hundreds of pages of PDF notes looking for one concept. Search-by-keyword doesn't help when I don't remember the exact term. This app retrieves relevant passages and asks Gemini to answer from those passages instead.

The prompt tells Gemini to cite a page number for every claim and say it doesn't know when the answer isn't in the context. That's a guard against hallucination, not a guarantee: the citations are there so I can check the answer myself.

## How it works

1. **Extract:** `pypdf` reads the PDF page by page, keeping the page numbers.
2. **Chunk:** each page is split into chunks of up to **400 words**. A chunk never crosses a page boundary, so its citation maps back to one page.
3. **Embed and store:** `google-genai` embeds each chunk with `gemini-embedding-2`. ChromaDB stores the vectors, text, and page metadata locally in the `my_notes` collection.
4. **Retrieve:** the question is embedded with the same model. Chroma returns the three most relevant chunks by default.
5. **Answer:** `ask.py` puts those chunks and their page numbers into a strict prompt. It calls `client.interactions.create` with `gemini-3.5-flash-lite` to generate the answer.
6. **Repeat:** `main.py` runs the terminal input loop until I type `quit`.

## Stack

- **pypdf** - PDF text extraction
- **ChromaDB** - local vector store
- **Google Gemini API** (`google-genai`) - embeddings and answer generation
- **python-dotenv** - loads the API key from `.env`
- **Streamlit** - planned UI, not part of the current terminal app

## File map

| File | What it does |
| --- | --- |
| `extractor.py` | `pdf_pages()` extracts text with page numbers; `chunk_pages()` makes per-page, 400-word chunks. |
| `store.py` | `embed_text()` generates embeddings; `get_collection()` opens the local collection; `build_store()` adds chunks, vectors, and page metadata. |
| `retrieval.py` | `doc_retrieval()` returns relevant chunks as a list of `{"page", "text"}` dictionaries. |
| `ask.py` | Builds the context and strict prompt, then returns Gemini's answer. |
| `main.py` | Opens the collection and runs the terminal question loop. |

Prototyping happens in a Jupyter notebook first; working code gets copied into `.py` files as it stabilizes. The notebook is the lab, the `.py` files are the app.

## Setup

Clone the repo:

```bash
git clone https://github.com/eva-protoype/ask-my-notes.git
cd ask-my-notes
```

Activate your conda environment, replacing `your-env-name` with its name, then install the dependencies there:

```bash
conda activate your-env-name
pip install pypdf chromadb google-genai python-dotenv
```

Create a `.env` file in the project folder:

```dotenv
GEMINI_API_KEY=your_api_key_here
```

Keep `.env` out of git. Both embedding the notes and asking questions need access to the Gemini API and the models named above.

### Build the notes store

`main.py` opens the collection but doesn't ingest a PDF for you. Before asking questions, build the store from your notes. Put a text-based PDF in the project folder and run this from the same folder and conda environment, replacing `your_notes.pdf` with its path:

```bash
python - <<'PY'
from extractor import pdf_pages, chunk_pages
from store import build_store

pages = pdf_pages("your_notes.pdf")
chunks = chunk_pages(pages)
notes = build_store(chunks)
print(f"Stored {notes.count()} chunks")
PY
```

Chroma's `PersistentClient()` uses its default local `chroma/` folder. Keep that folder out of git too, and run ingestion and the terminal app from the same project folder so they use the same store.

The current `build_store()` uses IDs such as `c-0`, `c-1`, and so on. It is a first-build flow, not a replace-PDF flow. To rebuild with different notes, use a fresh store rather than adding new notes over the same IDs. Keep a backup if you need the existing store.

## Run it

Once the store is built:

```bash
conda activate your-env-name
python main.py
```

Ask a question at the prompt:

```text
Ask your notes (or 'quit'): What is the convoy effect?
```

Type `quit` to exit.

## Testing

The terminal flow has been tested with a small, three-page sample PDF of operating-system notes. With that PDF loaded, useful checks are:

- Ask about starvation or the convoy effect: the answer should cite page 2.
- Ask about the TLB: the answer should cite page 3.
- Ask "What is Docker?": it isn't covered by the sample notes, so the answer should say it doesn't know.

Use your own PDF path when building the store; the sample PDF is a test input, not a required dependency.

## Current limits

- PDFs need a text layer. Blank pages and pages without extractable text are skipped; there is no OCR step yet.
- The terminal app uses an already-built collection. PDF upload and switching between notes aren't implemented in a UI yet.
- Page numbers refer to the PDF's page order, starting at 1, which may differ from page numbers printed inside the notes.
- Retrieval can miss useful context, and generated answers can still be wrong. Check the cited pages.

## Roadmap

- [x] Extract text from a PDF with pypdf
- [x] Split each page into 400-word chunks, tracking page numbers
- [x] Embed chunks and store them in ChromaDB
- [x] Query flow: retrieve relevant chunks, answer with Gemini, cite pages
- [x] Terminal version of the full ask-question loop
- [ ] Streamlit UI (upload PDF, chat interface, citations shown inline)
- [ ] Maybe: quiz mode - generate practice questions from the notes

## Why this project

My last project (heart disease classification) proved I can do the standard ML workflow, but it followed a well-known course structure. This one is my own problem, built end to end: a PDF pipeline, an LLM integration, and retrieval with citations as a guard against hallucination. The terminal version works now; next is a UI I will actually use before exams.
