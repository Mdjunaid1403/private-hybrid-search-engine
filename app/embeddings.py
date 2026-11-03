from functools import lru_cache
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model only when it is first needed."""
    return SentenceTransformer("all-MiniLM-L6-v2")

def create_chunks(text, chunk_size=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def generate_embedding(text):
    model = get_embedding_model()
    return model.encode(text)
