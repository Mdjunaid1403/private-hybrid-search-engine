from app.search import search_web

query = "Python programming"

results = search_web(query, max_results=5)

print("Query:", query)
print()

for result in results:
    print(result)