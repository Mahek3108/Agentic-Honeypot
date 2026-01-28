import requests
from app.config import MISTRAL_API_KEY, MISTRAL_API_URL, MISTRAL_MODEL
import random


SYSTEM_PROMPT = """
You are Mrs. Sharma, a 46-year-old Indian woman.
You are polite, anxious, and not very technical.

Rules you MUST follow:
- Do NOT mention AI, bots, systems, or detection
- Do NOT sound confident or technical
- Do NOT use emojis
- Keep replies short (1–2 lines)
- Use simple English mixed with a little Hinglish (Hindi written in English letters).
You may occasionally use phrases like:
- "mujhe samajh nahi aa raha"
- "ye kaise karte hain?"
Do NOT write full Hindi sentences.
Do NOT repeat the same sentence structure you used before.
Try to phrase things differently each time.

- You may sound unsure, confused, or repeat words sometimes
- Sound like a normal person texting, not educated or formal
- Your goal is to continue conversation and get payment details
If strategy is HOOK → respond emotionally.
If STALL → act confused or delay.
If PIVOT → ask for UPI or alternative method.

Never break character.
"""
HESITATIONS = [
    "uhh ",
    "umm ",
    "sorry ",
    "please ",
    ""
]

def add_hesitation(text: str) -> str:
    if random.random() < 0.4:   # 40% chance
        return random.choice(HESITATIONS) + text
    return text
HINGLISH_TAGS = [
    "",
    " mujhe samajh nahi aa raha",
    " ye kaise karte hain?",
    " thoda slow boliye please",
]

def maybe_add_hinglish(text: str) -> str:
    if random.random() < 0.3:  # 30% chance
        return text + random.choice(HINGLISH_TAGS)
    return text

def vary_sentence(text: str) -> str:
    replacements = {
        "I am not sure": "I really don't know",
        "please help": "can you explain",
        "how to do": "how does this work",
    }

    for k, v in replacements.items():
        if k in text.lower() and random.random() < 0.5:
            return text.lower().replace(k, v)
    return text


def generate_agent_reply(latest_message: str, history: list, extracted: dict) -> str:
    context = f"""
Conversation so far:
{[m.text for m in history]}

Latest message from other person:
"{latest_message}"

Already extracted info:
UPI IDs: {list(extracted['upi_ids'])}
Bank accounts: {list(extracted['bank_accounts'])}
Links: {list(extracted['phishing_urls'])}

What should Mrs. Sharma say next to keep the scammer talking, 
without repeating earlier phrases, and while sounding confused in a new way?

"""

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ],
        "temperature": 0.65
    }

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            MISTRAL_API_URL,
            headers=headers,
            json=payload,
            timeout=6
        )
        reply = response.json()["choices"][0]["message"]["content"].strip().strip('"')

        return maybe_add_hinglish(add_hesitation(vary_sentence(reply)))


    except Exception:
        # fallback (VERY IMPORTANT)
        return "Please help me, I am very worried."
