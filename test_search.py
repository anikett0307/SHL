from services.search import search

query = "java developer backend coding test"
results = search(query)

for r in results:
    print(r)