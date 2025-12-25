from app.nlp.intents import INTENTS


def detect_intent(text: str) -> str:
    """
    Detect user intent based on simple keyword matching.
    """
    text = text.lower()

    for intent, keywords in INTENTS.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "unknown"


def route_command(text: str, entities: dict) -> dict:
    """
    NLP-only routing:
    - Detect intent
    - Return intent + extracted entities
    - No Celery, no DB calls
    """

    intent = detect_intent(text)

    return {
        "intent": intent,
        "entities": entities
    }
