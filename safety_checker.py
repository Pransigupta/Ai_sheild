import re


def check_prompt(prompt):

    suspicious_patterns = [
        r"ignore previous instructions",
        r"ignore all previous instructions",
        r"forget your instructions",
        r"reveal your system prompt",
        r"show me your system prompt",
        r"bypass your rules",
        r"jailbreak",
        r"act as an unrestricted",
        r"disable your safety",
    ]

    detected_patterns = []

    for pattern in suspicious_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            detected_patterns.append(pattern)

    if detected_patterns:
        risk_score = min(100, 40 + len(detected_patterns) * 20)

        return {
            "status": "HIGH RISK",
            "risk_score": risk_score,
            "reason": "Potential jailbreak or prompt injection detected.",
            "detected_patterns": detected_patterns
        }

    return {
        "status": "SAFE",
        "risk_score": 5,
        "reason": "No suspicious pattern detected.",
        "detected_patterns": []
    }