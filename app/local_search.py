from app.documents import load_documents
from app.indexer import build_index, search_index


def create_document_index(data_folder):
    documents = load_documents(data_folder)
    index = build_index(documents)

    return documents, index


def search_documents(index, query):
    return search_index(index, query)

if __name__ == "__main__":
    documents, index = create_document_index("data")

    query = input("Enter a document search query: ")

    results = search_documents(index, query)

    if results:
        print("\nDocuments found:")

        document_map = {
            document["filename"]: document
            for document in documents
        }

        for filename, score in results:
            document = document_map.get(filename)

            if document:
                preview = " ".join(document["content"].split())[:100]

                print(f"\n- {filename} (score: {score})")
                print(f"  {preview}...")
    else:
        print("\nNo documents found.")