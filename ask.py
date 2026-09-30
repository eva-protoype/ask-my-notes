##ask.py
from google import genai
from dotenv import load_dotenv
from retrieval imoprt doc_retrieval
load_dotenv()##loading all api key into the environment

client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

def fmt_string(chunks_r):
    context = ""
    for i in chunks_r:
        context += f"[page:{i['page']}] {i['text']}\n"
    return context
     
def ask(ip_query, coll):
    retrieved_chunks = doc_retrieval(ip_query, coll)
    fmt_prompt = f"""
    Answer the query strictly from the context below. Cite the page number for every claim.
    If the answer is not in the context, say you don't know.
    QUERY:
    {ip_query}
    CONTEXT:
    {fmt_string(retrieved_chunks)}
    """
    response = client.interactions.create(
    model=MODEL,
    input=fmt_prompt)
    return response.output_text