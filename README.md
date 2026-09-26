# Ask My Notes

A RAG (retrieval-augmented generation) app for chatting with my own college notes. Upload a PDF of lecture notes, ask questions in plain English, and get answers that cite the exact page they came from - so nothing gets hallucinated and every claim can be checked against the source.

Built for my own exam prep first, and as a portfolio project for GenAI/ML internship applications.

> **Status: early build.** The project is in its first sessions. Right now it extracts text from a PDF. The sections below describe what works today, what the plan is, and how to run what exists.

## The idea

Before exams I end up digging through hundreds of pages of PDF notes looking for one concept. Search-by-keyword doesn't help when you don't remember the exact term. The plan:

1. Extract text from notes PDFs, keeping track of which page each piece of text came from.
2. Split the text into chunks (~500 tokens each) and embed them into a local vector database.
3. At question time, pull the 4-5 most relevant chunks and hand them to an LLM with a strict prompt: answer only from this context, and cite the page.
4. Wrap it all in a simple UI so asking a question feels like chatting with the notes.

## Stack (planned)

- **pypdf** - text extraction from PDFs
- **ChromaDB** - local vector store for chunk embeddings
- **Google Gemini API** (`google-genai`) - embeddings + answer generation, free tier
- **Streamlit** - the chat UI

## What works today

- PDF text extraction with `pypdf`: point the script at a notes PDF and it prints the extracted text page by page. This is the foundation everything else builds on - no clean text, no RAG.

Prototyping happens in a Jupyter notebook first; working code gets copied into `.py` files as it stabilizes.

## Roadmap

- [x] Extract text from a PDF with pypdf
- [ ] Split extracted text into ~500-token chunks, tracking page numbers
- [ ] Embed chunks and store them in ChromaDB
- [ ] Query flow: retrieve top-k chunks, answer with Gemini, cite pages
- [ ] Terminal version of the full ask-question loop
- [ ] Streamlit UI (upload PDF, chat interface, citations shown inline)
- [ ] Maybe: quiz mode - generate practice questions from the notes

## Running it (current state)

Requires Python 3.10+.

```bash
git clone https://github.com/eva-protoype/ask-my-notes.git
cd ask-my-notes
pip install pypdf
```

Then run the extraction on a PDF, or open the notebook and run the cells in order. Later milestones (ChromaDB, Gemini) will need extra dependencies and a `GEMINI_API_KEY` environment variable - setup instructions will land here as those pieces do.

## Why this project

My last project (heart disease classification) proved I can do the standard ML workflow, but it followed a well-known course structure. This one is my own problem, built end to end: a real data pipeline, an LLM integration, retrieval with citations as a guard against hallucination, and a UI I will actually use before exams.
