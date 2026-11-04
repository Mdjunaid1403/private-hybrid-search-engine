
from functools import lru_cache


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model only when first needed."""
    from fastembed import TextEmbedding

    return TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        threads=1,
    )


def create_chunks(text, chunk_size=50):
    """Split text into chunks of a fixed number of words."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks


def generate_embedding(text):
    """Generate a 384-dimensional embedding."""
    model = get_embedding_model()
    return next(model.embed([text]))