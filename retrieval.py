from store import embed_text

##now working on the retrieval file content which has functions for retrival of document from chroma db
def doc_retrieval(ip_query, notes, n_result=3):
    re_doc = []
    vectors = embed_text([ip_query])##using our vector function
    result = notes.query(
                query_embeddings=vectors,
                n_results=n_result
    )
    for i,j in zip(result['metadatas'][0],result['documents'][0]):
        re_doc.append({'page':i['page'], 'text':j})
    return re_doc