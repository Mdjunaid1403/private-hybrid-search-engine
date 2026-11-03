from pathlib import Path


def load_documents(data_folder):
    documents = []

    for file_path in Path(data_folder).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        documents.append({
            "filename": file_path.name.lower(),
            "content": content
        })

    return documents


if __name__ == "__main__":
    documents = load_documents("data")

    for document in documents:
        print(f"\nFile: {document['filename']}")
        print(f"Content: {document['content']}")