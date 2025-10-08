from textblob import TextBlob

def score_animal_record(data):
    fields = ['name', 'category', 'origin', 'sleep_pattern', 'food_habits', 'fun_facts']
    score = 0

    for field in fields:
        value = data.get(field, "")
        
        # Normalize fun_facts into a string for scoring
        if field == 'fun_facts':
            if isinstance(value, list):
                value = ' '.join(value)
            elif isinstance(value, dict):
                value = ' '.join(value.values())
            elif not isinstance(value, str):
                value = str(value)

        if isinstance(value, str) and len(value.strip()) > 5:
            score += 1

        # Add NLP sentiment bonus for fun facts
        if field == 'fun_facts':
            blob = TextBlob(value)
            if blob.sentiment.polarity > 0.1:
                score += 1

    final_score = min(score, 10)  # clamp to 10
    print(f"[Score Function] Animal: {data.get('name')} | Score: {final_score}")
    return final_score
