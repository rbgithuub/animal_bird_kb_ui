def animal_serializer(animal) -> dict:
    return {
        "id": str(animal["_id"]),
        "name": animal["name"],
        "category": animal["category"],
        "origin": animal["origin"],
        "sleep_pattern": animal["sleep_pattern"],
        "food_habits": animal["food_habits"],
        "fun_facts": animal["fun_facts"]
    }
