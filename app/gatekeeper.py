import re
import requests
from app.config import MISTRAL_API_KEY, MISTRAL_API_URL, MISTRAL_MODEL

SCAM_KEYWORDS = [
    "account blocked",
    "verify",
    "urgent",
    "click",
    "refund",
    "kyc"
]


def quick_rule_check(text: str) -> bool:
    text = text.lower()

    if re.search(r"http[s]?://", text):
        return True

    for kw in SCAM_KEYWORDS:
        if kw in text:
            return True

    return False


def llm_scam_check(text: str) -> bool:
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        "You are a fraud detection system.\n"
        "Is the following message a scam?\n\n"
        f"Message: {text}\n\n"
        "Respond ONLY with TRUE or FALSE."
    )

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(
            MISTRAL_API_URL,
            headers=headers,
            json=payload,
            timeout=5
        )

        result = response.json()["choices"][0]["message"]["content"].strip()
        return result.upper() == "TRUE"

    except Exception:
        # Fail-safe: assume scam if model fails
        return True


def detect_scam(text: str) -> bool:
    # Step 1: fast rule-based check
    if quick_rule_check(text):
        return True

    # Step 2: LLM-based decision
    return llm_scam_check(text)
