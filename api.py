from fastapi import FastAPI
from ask import ask
from pydantic import BaseModel
from store import list_subjects

class Query(BaseModel):
    query: str
    sub: str
app = FastAPI()

@app.post("/ask/")
def ask_query(query: Query):
    return ask(query.query, query.sub.upper())

@app.get("/subjects")
def subs():
    return list_subjects()
