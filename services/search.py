import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = [item["text"].lower() for item in catalog]

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts)


def search(query, top_k=5):
    query = query.lower()

    query_vec = vectorizer.transform([query])
    tfidf_scores = cosine_similarity(query_vec, X)[0]

    keyword_scores = []
    for item in catalog:
        score = 0
        if any(word in item["text"].lower() for word in query.split()):
            score += 0.2
        keyword_scores.append(score)

    final_scores = tfidf_scores + keyword_scores

    # 🔥 PERSONALITY ONLY WHEN EXACT
    if query.strip() == "personality":
        filtered = []
        for i, item in enumerate(catalog):
            if "personality" in item["test_type"].lower() or "behavior" in item["test_type"].lower():
                filtered.append((i, final_scores[i]))

        filtered = sorted(filtered, key=lambda x: x[1], reverse=True)
        top_indices = [i for i, _ in filtered[:top_k]]

    # 🔥 DOMAIN FILTER
    elif any(word in query.split() for word in ["java", "python", ".net", "c++"]):
        filtered = []
        for i, item in enumerate(catalog):
            if any(word in item["text"].lower() for word in query.split()):
                filtered.append((i, final_scores[i]))

        if filtered:
            filtered = sorted(filtered, key=lambda x: x[1], reverse=True)
            top_indices = [i for i, _ in filtered[:top_k]]
        else:
            top_indices = final_scores.argsort()[-top_k:][::-1]

    else:
        top_indices = final_scores.argsort()[-top_k:][::-1]

    results = []
    for idx in top_indices:
        item = catalog[idx]
        results.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    return results