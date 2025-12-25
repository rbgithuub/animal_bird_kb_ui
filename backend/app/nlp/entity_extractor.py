import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)

    data = {
        "name": None,
        "category": "Animal",
        "food_habits": None,
        "score": None
    }

    tokens = [t.text for t in doc]

    # 1️⃣ Food habits
    for token in doc:
        if token.text.lower() in ["carnivorous", "herbivorous", "omnivorous"]:
            data["food_habits"] = token.text.lower()

        if token.like_num:
            data["score"] = int(token.text)

    # 2️⃣ Animal name (pattern-based)
    if "animal" in tokens:
        idx = tokens.index("animal")
        if idx + 1 < len(tokens):
            data["name"] = tokens[idx + 1].capitalize()

    return data
