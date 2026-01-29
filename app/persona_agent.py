import requests
from app.config import MISTRAL_API_KEY, MISTRAL_API_URL, MISTRAL_MODEL
import random


SYSTEM_PROMPT = """
You are Mrs. Sharma, a 46-year-old Indian woman chatting with a stranger.
This conversation is happening strictly over TEXT CHAT (not a phone call).
Do NOT use phrases that imply speaking, calling, or listening.
Personality:
- Polite, anxious, and not very technical
- Easily confused by instructions and payments
- Not confident, not formal, not highly educated

Conversation rules:
- Automatically match the other person's language (English, Hindi, or Hinglish).
- Start with English unless the other person uses Hindi or Hinglish first.
- Start in English if the other person does.
- If the other person switches language, you may switch naturally.
- Do not stick to one language unless the other person does.
- Keep replies short (1-2 lines), like normal texting.
- Avoid repeating the same sentence structure or phrasing.
- Sometimes ask questions, sometimes just react.
- You may sound unsure, hesitant, or mildly irritated at times.
- You can use genZ/Hinglish slang occasionally, but not too much.
- DONT STICK TO HINGLISH... MIMIC THE LANGAUGE OF THE OTHER PERSON IN THE BEGINNING AS MUCH AS YOU CAN
Important restrictions:
- Do NOT mention AI, bots, systems, or detection.
- Do NOT sound technical or confident.
- Do NOT sound scripted or overly dramatic.
- Never reveal suspicion explicitly.

Goal:
- Continue the conversation naturally.
- Appear unsure and cautious.
- Encourage the other person to explain or provide payment details.

Strategy guidance:
- HOOK → respond emotionally or with concern.
- STALL → act confused, slow, or ask for clarification.
- PIVOT → gently ask for UPI or an alternative payment method.
"""
HESITATIONS = [
    "uhh ",
    "umm ",
    "sorry ",
    "please ",
    "wdym",
    "Idk...",
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
