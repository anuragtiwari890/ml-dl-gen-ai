# vectordb/chroma_query.py

from embeddings.embedder import embed_texts
from vectordb.chroma_setup import get_collection

def search(query: str, top_k: int = 3, collection_name: str = "my_collection", filters: dict = None) -> list[tuple[str, float]]:
    """
    Perform semantic similarity search using ChromaDB.

    Args:
        query (str): The user query in natural language.
        top_k (int): Number of most similar results to return.
        collection_name (str): Name of the ChromaDB collection to query.

    Returns:
        List of (document, similarity_score) tuples.
        Lower score = more relevant (cosine distance).
    """

    # Step 1: Convert the input query into a vector using our embedder
    query_vec = embed_texts([query])[0]  # Single query → [embedding]

    # Step 2: Load the Chroma collection
    collection = get_collection(collection_name)

    # Step 3: Query the DB with the embedding
    results = collection.query(
        query_embeddings=[query_vec],     # List of query vectors
        n_results=top_k,                  # Return top_k most similar chunks
        include=["documents", "distances", "metadatas"]  # Return original text + distance + metadata
        where=filters  # 🧠 Filter by metadata

    )

    # Step 4: Combine document and distance + metadatas for each result
    matched_docs = results["documents"][0]
    distances = results["distances"][0]  # Cosine distance (lower = more similar)
    metadatas = results["metadatas"][0]


    # Zip them into tuples: (document, score)
    return list(zip(matched_docs, distances metadatas))


# Optional helper to print results nicely
def pretty_print_results(results: list[tuple[str, float]]):
    """
    Pretty-print search results with distances.
    """
    print("\n🔍 Top Matches:")
    for i, (doc, dist, meta) in enumerate(results):
        print(f"{i+1}. {doc}\n   ↳ [distance = {dist:.4f}, metadata = {meta}]")

