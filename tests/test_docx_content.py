from app.database import get_documents_for_search


documents = get_documents_for_search()

for document in documents:
    if document["filename"] == "SIR DRAFT LIST (118).docx":
        print("Document found.")
        print("Content length:", len(document["content"]))
        print("\nContent:")
        print(document["content"])
        break
else:
    print("Document not found.")