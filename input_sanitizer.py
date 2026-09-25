def sanitize_prompt(prompt):

    # Remove extra spaces
    prompt = prompt.strip()

    # Replace multiple spaces with one space
    prompt = " ".join(prompt.split())

    return prompt