import string
import unicodedata
from app.documents import load_documents
from rapidfuzz import fuzz

STOP_WORDS = {
    "a", "an", "the",
    "is", "are", "was", "were",
    "and", "or", "but",
    "of", "to", "in", "on",
    "for", "with", "as", "by",
    "from", "at", "this", "that"
}

def normalize_word(word):
    word = unicodedata.normalize(
        "NFKC",
        word
    )

    word = word.lower().strip()

    word = word.strip(
        string.punctuation
    )

    # Remove invisible Unicode formatting characters
    word = "".join(
        character
        for character in word
        if unicodedata.category(character) != "Cf"
    )

    return word

def build_index(documents):
    index = {}

    for document in documents:
        filename = document["filename"]
        words = document["content"].split()
        unique_words = dict.fromkeys(
            normalize_word(word) for word in words
        )

        for word in unique_words:
            if not word or word in STOP_WORDS:
                continue

            if word not in index:
                index[word] = []

            index[word].append(filename)

    return index


def search_index(index, query):
    if not query.strip():
        return []

    words = []

    for word in query.split():
        normalized = normalize_word(word)

        if normalized and normalized not in STOP_WORDS:
            if normalized not in words:
                words.append(normalized)

    scores = {}

    for word in words:
        # First, look for an exact match.
        word_results = index.get(word, [])

        for filename in word_results:
            scores[filename] = scores.get(filename, 0) + 1

        # If no exact match exists, look for close spelling matches.
        if not word_results:
            for indexed_word, filenames in index.items():
                similarity = fuzz.ratio(word, indexed_word)

                # Require a high similarity to reduce irrelevant matches.
                if similarity >= 85:
                    for filename in filenames:
                        scores[filename] = scores.get(filename, 0) + 1

    ranked_results = sorted(
        scores.items(),
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