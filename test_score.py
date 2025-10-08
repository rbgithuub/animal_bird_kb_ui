from worker.utils.score_calculator import score_animal_record

# Example test data (you can tweak this)
test_data = {
    "name": "f",
    "category": "d",
    "origin": "",
    "sleep_pattern": "P and ",
    "food_habits": "g",
    "fun_facts": [
        "",
        "U"
    ]
}

# Call scoring function
score = score_animal_record(test_data)

# Display output
print(f"Score for {test_data['name']}: {score}")
