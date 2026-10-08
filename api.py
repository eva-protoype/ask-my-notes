from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from hashlib import sha1
from io import BytesIO
from extractor import pdf_pages, chunk_pages
from store import build_store
from ask import ask
from store import list_subjects

class Query(BaseModel):
    query: str
    sub: str

app = FastAPI()

@app.post("/ask/")
async def ask_query(query: Query):
    return ask(query.query, query.sub)

@app.get("/subjects")
async def list_subject_routes():
    return list_subjects()

## an ingest endpoint now which takes file and adds it to the db
@app.post("/ingest/")
async def create_upload_file(file: UploadFile, sub:str = Form(...)):
    contents = await file.read()
    pages = pdf_pages(BytesIO(contents))
    chunks = chunk_pages(pages)
    notes = build_store(chunks, sub, file.filename, sha1(contents).hexdigest())
    return notes.count()
    