# 🧠 ChromaDB Vector DB Playground (No LLM)

A clean and minimal learning-focused codebase to deeply understand how Vector Databases like **ChromaDB** work — from embedding to querying, indexing, metadata filtering, and storage inspection.

---

## 📦 Features

| Feature                         | Description |
|--------------------------------|-------------|
| ✅ File-based embedding         | Embed raw `.txt` files using sentence-transformers |
| ✅ ChromaDB indexing            | Add documents into persistent Chroma collections |
| ✅ Metadata tagging             | Attach metadata like source file, chunk index |
| ✅ Semantic query engine        | Search using cosine distance with top-k matches |
| ✅ Metadata filtering           | Retrieve docs matching a metadata filter (e.g., filename) |
| ✅ Result ranking + scores      | Show cosine distance scores for relevance |
| ✅ Pretty terminal output       | Simple terminal UI for Q&A loop |
| ✅ Explore physical storage     | Inspect DuckDB and Parquet files behind ChromaDB |

---

## 📁 Project Structure 
<pre> ├── app.py                  # Entry point CLI for asking semantic questions 
├── data/                   # Directory for input `.txt` files 
│    └── sample.txt         # Example document for embedding and search 
├── requirements.txt        # Python dependencies 
├── vectordb/ 
│    ├── chroma_setup.py    # Initializes ChromaDB client and collection 
│    ├── chroma_add.py      # Embeds and adds documents to the DB 
│    └── chroma_query.py    # Handles semantic search + metadata filtering 
└── chroma_store/           # Auto-created persistent ChromaDB storage </pre>

## 🚀 How to Run

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv simple-vector
source simple-vector/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Add Your Text File

Place a `.txt` file inside the `data/` directory (e.g., `sample.txt`).

### 3. Run the CLI App

```bash
python app.py
```

Example output:

```
Ask a question (or 'exit'): what is chromadb
Filter by source (or press Enter to skip): data/sample.txt

🔍 Top Matches:
1. ChromaDB is a vector store... (distance = 0.21, metadata = {...})
```

---

## 🧰 Internals Explained

- **Embeddings**: Uses `sentence-transformers` to embed chunks into dense vectors.
- **Storage**: Chroma uses `duckdb+parquet` under the hood; all vectors are persisted on local disk.
- **Search**: Based on cosine distance (lower = more relevant).
- **Filtering**: Apply metadata filters (e.g., source filename) to narrow results.

---

## 🔍 Explore Vector DB Internals

You can inspect the database using DuckDB CLI or pandas.

```bash
# Enter DuckDB shell
duckdb chroma_store/tenant.db
```

Within DuckDB shell:

```sql
SELECT * FROM 'chroma_store/collections/<collection_id>/documents.parquet';
SELECT * FROM 'chroma_store/collections/<collection_id>/embeddings.parquet';
```

Or using Python:

```python
import pandas as pd
df = pd.read_parquet("chroma_store/collections/<collection_id>/documents.parquet")
print(df.head())
```

---

## 📚 Learning Objectives

- Understand how vector DBs **index** and **search** embeddings
- Learn how **metadata filters** and **distances** affect retrieval
- Build foundation to later integrate with LLMs (RAG pipeline)

---

## 📌 Roadmap

- [ ] Add document deletion and updating
- [ ] Improve text chunking (e.g., sentence-based)
- [ ] Compare with FAISS
- [ ] Visualize embedding clusters (UMAP/t-SNE)
- [ ] Optional: integrate Ollama open-source LLMs later

---

## 📦 Requirements

- Python 3.9+
- sentence-transformers
- chromadb
- duckdb
- pandas

See `requirements.txt` for full dependency list.

---

## 🧑‍💻 Author & License

Built by Anurag Tiwari as part of a deep dive into GenAI infrastructure.  
Feel free to fork, clone, and customize for learning or production.  
**License: MIT**
