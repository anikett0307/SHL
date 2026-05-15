import json

with open("data/raw_catalog.json", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

content = content.replace("\n", " ").replace("\r", " ")

data = json.loads(content)

# print first 3 items fully
for i in range(3):
    print("\nITEM", i)
    print(data[i])