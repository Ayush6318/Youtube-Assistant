from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    return splitter.create_documents(
        [text]
    )