"""
This module is responsible for querying the Chroma vector store
using a natural language query. It returns the most relevant 
code or document chunks that match the query using cosine similarity.
"""

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Path to the persisted Chroma vector database
CHROMA_DB_DIR = "chroma_db"

# Load the same embedding model used during the embedding phase
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

def retrieve_relevant_chunks(query, top_k=3, persist_directory=CHROMA_DB_DIR):
    """
    Retrieve top-k relevant chunks from Chroma vector store for a given query.

    Args:
        query (str): User's question or search input.
        top_k (int): Number of top matching chunks to return.
        persist_directory (str): Path to the Chroma DB directory.

    Returns:
        List[dict]: A list of dictionaries containing:
            - 'content': The retrieved chunk's content
            - 'metadata': Source metadata (e.g., file path)
    """

    # Load the vector store from disk using the embedding model
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )

    # Perform semantic similarity search on vector DB
    docs = vectordb.similarity_search(query, k=top_k)

    # Format the results
    return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]



def get_code_files_from_repo(repo_path, extensions=(".py", ".js", ".ts", ".java", ".cpp")):
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                        code_files.append({
                            "path": os.path.relpath(file_path, repo_path),  # relative to repo root
                            "code": code
                        })
                except Exception as e:
                    print(f"⚠️ Skipped {file_path}: {e}")
    return code_files
