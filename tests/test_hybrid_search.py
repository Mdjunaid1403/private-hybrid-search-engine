from hybrid_search import hybrid_search


query = "How do computers learn from data?"

results = hybrid_search(query)

print("Query:", query)
print()

for result in results:
    print(result)