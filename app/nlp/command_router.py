from app.nlp.intents import INTENTS
from app.tasks.animal_tasks import (
    create_animal,
    update_animal,
    delete_animal,
    fetch_animals
)

def detect_intent(text):
    for intent, keywords in INTENTS.items():
        if any(k in text.lower() for k in keywords):
            return intent
    return "unknown"

def route_command(text, entities):
    intent = detect_intent(text)

    if intent == "create":
        create_animal.delay(entities)
        return "Create task submitted"

    if intent == "read":
        return fetch_animals.delay(entities).get()

    if intent == "update":
        update_animal.delay(entities)
        return "Update task submitted"

    if intent == "delete":
        delete_animal.delay(entities)
        return "Delete task submitted"

    return "Unknown command"
