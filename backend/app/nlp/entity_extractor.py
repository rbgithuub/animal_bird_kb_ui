import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)

    data = {
        "name": None,
        "category": "Animal",
        "food_habits": None,
        "fun_facts": [],
        "score": 0
    }

    # food habits
    for token in doc:
        if token.text.lower() in ["carnivorous", "herbivorous", "omnivorous"]:
            data["food_habits"] = token.text.capitalize()

        if token.like_num:
            data["score"] = min(int(token.text), 10)

    # name detection (domain rule)
    tokens = [t.text for t in doc]
    if "animal" in tokens:
        idx = tokens.index("animal")
        if idx + 1 < len(tokens):
            data["name"] = tokens[idx + 1].capitalize()

    # fun facts (semicolon logic)
    if "fun fact" in text.lower():
        facts = text.split(":")[-1]
        data["fun_facts"] = [f.strip() for f in facts.split(";")][:2]

    # auto score heuristic
    data["score"] = calculate_score(data)

    return data
