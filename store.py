##embeding the chunks that we made in extractor.py
import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()##loading the environment vars in the OS

client = genai.Client()
EMBED_M = "gemini-embedding-2"

def embed_text(texts):
    vectors = []
    for text in texts:
        result = client.models.embed_content(
            model=EMBED_M,
            contents=text)
        vectors.append(result.embeddings[0].values)
    return vectors
    
def get_collection():
    chroma_client = chromadb.PersistentClient()
     return chroma_client.get_or_create_collection(name="my_notes")

def build_store(chunks):
    notes = get_collection()
    vector = embed_text([c["text"] for c in chunks])
    notes.add(
                    ids=[f"c-{i}" for i in range(0,len(chunks))],
                    embeddings=vector,
                    documents=[c["text"] for c in chunks],
                    metadatas=[{"page":c["page"]} for c in chunks],) ##meta data is always list of dicts
    #print(notes.count()) just for checking purposes
    return notes