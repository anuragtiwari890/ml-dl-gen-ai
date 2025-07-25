# retriever/test_retriever.py

from retriever import retrieve_relevant_chunks

def test_retriever():
    query = "How does the embedding process work?"  # example query
    results = retrieve_relevant_chunks(query, top_k=3)

    print("\n=== Top Relevant Chunks ===\n")
    for i, doc in enumerate(results, 1):
        print(f"[{i}] {doc.page_content}\n")

if __name__ == "__main__":
    test_retriever()
