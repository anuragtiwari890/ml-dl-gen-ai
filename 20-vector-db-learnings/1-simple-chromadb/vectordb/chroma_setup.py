# vectordb/chroma_setup.py

import chromadb
import os

def get_collection(name="my_collection"):
    """
    Create or load a ChromaDB collection using the new Client API.

    - Uses chromadb.PersistentClient (instead of old Client + Settings).
    - Local DuckDB+Parquet-based vector store.
    """

    persist_path = os.path.abspath("./chroma_store")

    # ✅ New way to use persistent Chroma client
    client = chromadb.PersistentClient(path=persist_path)

    try:
        return client.get_collection(name)
    except:
        return client.create_collection(name)
