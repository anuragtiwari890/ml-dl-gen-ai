# embeddings/embedder.py

# Import a lightweight, pretrained SentenceTransformer model
from sentence_transformers import SentenceTransformer

# Load the model. This will download 'all-MiniLM-L6-v2' if not cached.
# Produces 384-dimensional embeddings, good balance of speed and quality.
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Takes a list of text chunks and returns their embeddings (as list of vectors).
    Embeddings are what will be stored in the vector database.
    """
    return model.encode(texts, show_progress_bar=True).tolist()
