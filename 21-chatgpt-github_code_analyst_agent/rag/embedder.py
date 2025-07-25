from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

def run_embedding_pipeline_all_files(code_files: dict[str, str], persist_directory="chroma_db"):
    # code_files is a dict of {filename: file_content}
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    documents = []
    for file_name, file_content in code_files.items():
        doc = Document(page_content=file_content, metadata={"source": file_name})
        documents.append(doc)

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    vectordb.persist()
    return vectordb


