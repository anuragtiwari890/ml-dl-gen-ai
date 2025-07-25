# vectordb/chroma_add.py

from embeddings.embedder import embed_texts
from vectordb.chroma_setup import get_collection

def load_text(path):
    """
    Load and split the input file into paragraphs/chunks.
    You can later replace this with sentence or token-level chunking.
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split based on double newlines (paragraphs)
    return [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]

def add_documents(path, collection_name="my_collection"):
    """
    - Loads a file and splits into chunks.
    - Converts each chunk to a dense embedding.
    - Adds all chunks and embeddings to ChromaDB.
    """

    chunks = load_text(path)
    embeddings = embed_texts(chunks)

    # Generate unique IDs for each chunk
    ids = [f"doc-{i}" for i in range(len(chunks))]

    # Load or create the collection
    collection = get_collection(collection_name)

    # Add documents (text + embedding + ID)
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

    print(f"✅ Indexed {len(chunks)} chunks.")

# vectordb/chroma_add.py

from embeddings.embedder import embed_texts
from vectordb.chroma_setup import get_collection
import uuid

def add_documents(file_path, collection_name="my_collection"):
    """
    - Loads a file and splits into chunks.
    - Converts each chunk to a dense embedding.
    - Adds all chunks and embeddings to ChromaDB.
    """


    with open(file_path, "r", encoding="utf-8") as f:   # Load and split the input file into paragraphs/chunks.
        content = f.read()

    chunks = content.split("\n")  # You can use a better splitter later
    embeddings = embed_texts(chunks)

    collection = get_collection(collection_name)

    # Example: Add filename and index as metadata
    metadatas = [{"source": file_path, "chunk_index": i} for i in range(len(chunks))]

    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ Added {len(chunks)} chunks to collection '{collection_name}'")

