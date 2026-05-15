from services.search import search
import json

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def is_vague(text):
    return len(text.split()) < 4


def find_test_by_name(name):
    for item in catalog:
        if name.lower() in item["name"].lower():
            return item
    return None


def handle_chat(messages):
    last_user_msg = messages[-1]["content"].lower()

    # OUT OF SCOPE
    if any(word in last_user_msg for word in ["salary", "legal", "law", "policy", "interview tips"]):
        return {
            "reply": "I can only help with SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # COMPARISON
    if "compare" in last_user_msg:
        text = last_user_msg.replace("compare", "").strip()

        if "and" in text:
            parts = text.split("and")
        elif "vs" in text:
            parts = text.split("vs")
        else:
            parts = []

        if len(parts) >= 2:
            name1 = parts[0].strip()
            name2 = parts[1].strip()

            test1 = find_test_by_name(name1)
            test2 = find_test_by_name(name2)

            if test1 and test2:
                return {
                    "reply": f"{test1['name']} focuses on {test1['test_type']}. {test2['name']} focuses on {test2['test_type']}.",
                    "recommendations": [],
                    "end_of_conversation": False
                }

        return {
            "reply": "I couldn't find both assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # 🔥 STRICT REFINEMENT (ONLY SHORT COMMAND)
    if last_user_msg.strip() in ["add personality test", "add personality", "personality test"]:
        results = search("personality", top_k=5)
        return {
            "reply": "I've updated the recommendations based on your new requirement.",
            "recommendations": results,
            "end_of_conversation": False
        }

    # VAGUE
    if is_vague(last_user_msg):
        return {
            "reply": "Please specify role, experience level, and key skills required.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # 🔥 STRICT DOMAIN SEARCH (NO MIXED QUERY ISSUE)
    clean_query = last_user_msg

    # REMOVE noise words
    for word in ["add", "also", "personality"]:
        clean_query = clean_query.replace(word, "")

    results = search(clean_query.strip(), top_k=5)

    return {
        "reply": "Based on your requirements, here are the most relevant SHL assessments:",
        "recommendations": results,
        "end_of_conversation": False
    }