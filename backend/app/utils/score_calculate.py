def calculate_score(data):
    score = 0
    if data["name"]: score += 3
    if data["food_habits"]: score += 2
    if len(data["fun_facts"]) >= 2: score += 3
    return min(score, 10)
