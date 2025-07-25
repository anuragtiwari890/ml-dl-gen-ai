# app.py

from vectordb.chroma_add import add_documents
from vectordb.chroma_query import search, pretty_print_results

if __name__ == "__main__":
    add_documents("data/sample.txt")  # Index your file once

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == 'exit':
            break

        # You can adjust top_k as needed (try top_k=1 to restrict)
        results = search(q, top_k=2)

        # Show the results with distance scores
        pretty_print_results(results)
