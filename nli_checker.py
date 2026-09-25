import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "cross-encoder/nli-MiniLM2-L6-H768"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)


def check_nli(source, answer):

    if source.strip() == "" or answer.strip() == "":
        return {
            "factuality_score": 0,
            "status": "NO SOURCE OR ANSWER",
            "method": "NLI"
        }

    inputs = tokenizer(
        source,
        answer,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)[0]

  

    entailment_score = probabilities[1].item()

    factuality_score = round(entailment_score * 100, 2)

    if factuality_score >= 70:
        status = "CONSISTENT"
    elif factuality_score >= 40:
        status = "PARTIALLY CONSISTENT"
    else:
        status = "LOW CONSISTENCY"

    return {
        "factuality_score": factuality_score,
        "status": status,
        "method": "NLI"
    }