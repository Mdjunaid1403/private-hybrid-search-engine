from sentence_transformers import SentenceTransformer

def create_chunks(text, chunk_size=50):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully")

with open("test_document.txt", "r", encoding="utf-8") as file:
    text = file.read()

print(text)

chunks = create_chunks(text, chunk_size=10)

print(chunks)

embeddings = model.encode(chunks)

print(embeddings.shape)

print(embeddings[0])

for i in range(len(chunks)):
    print("Chunk:", chunks[i])
    print("Embedding shape:", embeddings[i].shape)
    print()



# documents = [
#     "Python is a programming language",
#     "FastAPI is a Python framework for building APIs",
#     "Dogs are loyal and friendly animals"
# ]

# embeddings = model.encode(documents)

# print(embeddings)

# print(embeddings.shape)