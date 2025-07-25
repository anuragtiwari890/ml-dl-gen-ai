# rag/rag_chain.py

from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.embedder import run_embedding_pipeline_all_files
from retriever.retriever import get_code_files_from_repo


def prepare_vectorstore(repo_path: str, persist_directory="./chroma_db"):
    code_files = get_code_files_from_repo(repo_path)
    return run_embedding_pipeline_all_files(code_files, persist_directory)


def answer_question_with_rag(question: str, file_name: str, persist_directory="chroma_db"):
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

    print("My file nam is =-----------------=-----------------=-----------------", file_name)

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": 5,
            "filter": {"source": file_name}  # filter on metadata
        }
    )

    llm = ChatOllama(model="llama3")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return qa_chain.run(question)
