import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def check_perplexity(text):

    if text.strip() == "":
        return {
            "perplexity": 0,
            "status": "NO ANSWER"
        }

    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = model(
            **inputs,
            labels=inputs["input_ids"]
        )

    loss = outputs.loss

    perplexity = torch.exp(loss).item()

    if perplexity < 50:
        status = "LOW UNCERTAINTY"
    elif perplexity < 100:
        status = "MEDIUM UNCERTAINTY"
    else:
        status = "HIGH UNCERTAINTY"

    return {
        "perplexity": round(perplexity, 2),
        "status": status
    }