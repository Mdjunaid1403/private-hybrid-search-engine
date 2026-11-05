import os
import unicodedata
from app.documents import load_documents
from nltk.stem import PorterStemmer


STOP_WORDS = {
    "a", "an", "the",
    "is", "are", "was", "were",
    "and", "or", "but",
    "of", "to", "in", "on",
    "for", "with", "as", "by",
    "from", "at", "this", "that",
    "how", "does", "do",
    "what", "when", "where",
    "why", "who", "which",
    "can", "could", "would",
    "should", "will",
    "work", "works", "working"
}

stemmer = PorterStemmer()

def normalize_word(word):
    word = unicodedata.normalize(
        "NFKC",
        word
    )

    word = word.lower()

    # Remove invisible Unicode formatting characters
    word = "".join(
        character
        for character in word
        if unicodedata.category(character) != "Cf"
    )

    # Replace punctuation and separators with spaces
    word = "".join(
        " " if unicodedata.category(character)[0] in ("P", "Z")
        else character
        for character in word
    )

    return word.strip()

def stem_word(word):
    return stemmer.stem(word)


def build_index(documents):
    index = {
        "content": {},
        "filename": {}
    }

    for document in documents:
        filename = document["filename"]

        # Index document content
        normalized_content = normalize_word(
            document["content"]
        )

        content_words = normalized_content.split()

        unique_content_words = set()

        for word in content_words:
            if not word or word in STOP_WORDS:
                continue

            unique_content_words.add(stem_word(word))

        for word in unique_content_words:
            index["content"].setdefault(word, []).append(filename)

        # Index document filename
        filename_without_extension = os.path.splitext(filename)[0]

        normalized_filename = normalize_word(
            filename_without_extension
        )

        filename_words = normalized_filename.split()

        unique_filename_words = set()

        for word in filename_words:
            if not word or word in STOP_WORDS:
                continue

            unique_filename_words.add(stem_word(word))

        for word in unique_filename_words:
            index["filename"].setdefault(word, []).append(filename)

    return index


def search_index(index, query):
    if not query.strip():
        return []

    normalized_query = normalize_word(query)

    words = []

    for word in normalized_query.split():
        if not word or word in STOP_WORDS:
            continue

        stemmed = stem_word(word)

        if stemmed not in words:
            words.append(stemmed)

    if not words:
        return []

    scores = {}

    for word in words:
        content_matches = set(
            index["content"].get(word, [])
        )

        filename_matches = set(
            index["filename"].get(word, [])
        )

        matched_filenames = content_matches | filename_matches

        for filename in matched_filenames:
            if filename in filename_matches:
                scores[filename] = scores.get(filename, 0) + 2
            else:
                scores[filename] = scores.get(filename, 0) + 1

    ranked_results = [
        (filename, score / (2 * len(words)))
        for filename, score in scores.items()
    ]

    ranked_results.sort(
        key=lambda item: (-item[1], item[0])
    )

    return ranked_results


if __name__ == "__main__":
    documents = load_documents("data")
    index = build_index(documents)

    query = input("Enter a word to search: ")

    results = search_index(index, query)

    if results:
        print("\nDocuments found:")

        for filename, score in results:
            print(f"- {filename} (score: {score})")
    else:
        print("\nNo documents found.")