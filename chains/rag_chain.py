from langchain_classic.chains.combine_documents import (
  create_stuff_documents_chain
)

from langchain_classic.chains import create_retrieval_chain

from prompts.rag_prompt import rag_prompt

def get_rag_chain(
    llm,retriever
):
  document_chain = (
    create_stuff_documents_chain(
      llm,rag_prompt
    )
  )

  rag_chain = create_retrieval_chain(
    retriever,document_chain
  )

  return rag_chain



  