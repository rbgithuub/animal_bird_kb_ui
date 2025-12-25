import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text.lower())

    data = {
        "name": None,
        "category": None,
        "food_habits": None,
        "score": None
    }

    for token in doc:
        if token.like_num:
            data["score"] = int(token.text)

        if token.text in ["carnivorous", "herbivorous", "omnivorous"]:
            data["food_habits"] = token.text

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            data["name"] = ent.text.capitalize()

    if "bird" in text:
        data["category"] = "Bird"
    else:
        data["category"] = "Animal"

    return data
