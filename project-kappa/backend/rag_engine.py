import json
import os

# Load the knowledge base
KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/knowledge_base.json")

def load_knowledge_base():
    try:
        with open(KB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_sovereign_alternatives(ai_response: str) -> list:
    """
    Given a displaced AI response, retrieve relevant African alternatives
    from the knowledge base based on keyword matching.
    """
    kb = load_knowledge_base()
    if not kb:
        return []

    response_lower = ai_response.lower()
    matches = []

    for entry in kb:
        keywords = entry.get("keywords", [])
        score = sum(1 for kw in keywords if kw.lower() in response_lower)
        if score > 0:
            matches.append({
                "score": score,
                "entry": {
                    "name": entry["name"],
                    "country": entry["country"],
                    "description": entry["description"],
                    "url": entry["url"],
                    "type": entry["type"]
                }
            })

    matches.sort(key=lambda x: x["score"], reverse=True)
    top = [m["entry"] for m in matches[:3]]

    return top