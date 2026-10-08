##embeding the chunks that we made in extractor.py
import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()##loading the environment vars in the OS

client = genai.Client()
EMBED_M = "gemini-embedding-001"##changing the model back to 001 for individual embeddings for each chunk (not aggregated)

chroma_client = chromadb.PersistentClient()

def embed_text(texts):
    result = client.models.embed_content(
            model=EMBED_M,
            contents=texts)
    return [e.values for e in result.embeddings]

def get_collection(subject):
    coll_name = "notes-" + subject.upper()
    return chroma_client.get_or_create_collection(name=coll_name)

def build_store(chunks,subject,file_name,file_hash):
    notes = get_collection(subject)
    vector = embed_text([c["text"] for c in chunks])
    notes.delete(
                	where={"source" : file_name})
    notes.upsert(
                    ids = [f"{file_hash}-{i}" for i in range(len(chunks))],
                    embeddings=vector,
                    documents=[c["text"] for c in chunks],
                    metadatas=[{"page":c["page"], "source":file_name} for c in chunks],) ##meta data is always list of dicts
    #print(notes.count()) just for checking purposes
    return notes

def list_subjects():
    return [i.name[6:] for i in chroma_client.list_collections()]