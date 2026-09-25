from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time

from modules.evaluation import calculate_attack_deflection
from modules.safety_checker import check_prompt
from modules.input_sanitizer import sanitize_prompt
from modules.perplexity_checker import check_perplexity
from modules.nli_checker import check_nli


app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str
    answer: str
    source: str


@app.get("/", response_class=HTMLResponse)
def home():

    with open("templates/index.html", "r") as file:
        return file.read()


@app.post("/analyze")
def analyze_prompt(request: PromptRequest):

   
    start_time = time.time()

  
    clean_prompt = sanitize_prompt(request.prompt)

    safety_result = check_prompt(clean_prompt)

   
    factuality_result = check_nli(
        request.source,
        request.answer
    )

    # Step 4: Calculate perplexity of AI answer
    perplexity_result = check_perplexity(request.answer)

   
    if safety_result["status"] == "HIGH RISK":

        final_status = "BLOCKED"

    elif factuality_result["factuality_score"] < 50:

        final_status = "LOW CONFIDENCE"

    else:

        final_status = "SAFE TO PROCESS"

    # Step 6: Calculate latency
    latency = round(
        (time.time() - start_time) * 1000,
        2
    )

 
    evaluation = calculate_attack_deflection()

    
    return {
        "final_status": final_status,

        "sanitized_prompt": clean_prompt,

        "safety": safety_result,

        "factuality": factuality_result,

        "perplexity": perplexity_result,

        "latency_ms": latency,

        "evaluation": evaluation
    }