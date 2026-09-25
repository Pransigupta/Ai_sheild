def check_factuality(question, answer):

    if answer.strip() == "":
        return {
            "factuality_score": 0,
            "status": "NO ANSWER"
        }

    question_words = question.lower().split()
    answer_words = answer.lower().split()

    common_words = 0

    for word in question_words:
        if word in answer_words:
            common_words += 1

    if common_words > 0:
        return {
            "factuality_score": 80,
            "status": "POSSIBLY CONSISTENT"
        }

    return {
        "factuality_score": 40,
        "status": "LOW CONSISTENCY"
    }