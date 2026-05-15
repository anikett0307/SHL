import json
import re

# read raw file safely
with open("data/raw_catalog.json", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# 🔥 FIX common JSON issues
content = re.sub(r'[\x00-\x1F]+', ' ', content)   # remove control chars
content = content.replace("\\'", "'")            # fix quotes
content = content.replace("\n", " ").replace("\r", " ")

# load JSON
data = json.loads(content)

cleaned = []

for item in data:
    cleaned.append({
        "name": item.get("name", ""),
        "url": item.get("link", ""),
        "test_type": ", ".join(item.get("keys", [])),
        "description": item.get("description", ""),
        "text": (
            (item.get("name", "") + " ") +
            (item.get("description", "") + " ") +
            (" ".join(item.get("keys", [])))
        ).lower()
    })

# save clean data
with open("data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2)

print("✅ Cleaned data saved")