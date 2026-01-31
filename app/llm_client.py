import requests
from app.config import MISTRAL_API_KEY, MISTRAL_API_URL, MISTRAL_MODEL


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.6) -> str:
    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature
    }

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        MISTRAL_API_URL,
        headers=headers,
        json=payload,
        timeout=6
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
