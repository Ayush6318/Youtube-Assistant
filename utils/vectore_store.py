from langchain_community.vectorstores import FAISS

def create_vector_store(
    documents,
    embedding
):
  db = FAISS.from_documents(
    documents,embedding

  )
  return db