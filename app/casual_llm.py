from app.config import LLM_CLIENT

def generate_casual_reply(text: str) -> str:
    """
    Lightweight LLM call for normal conversation.
    NO scam logic. NO memory. NO extraction.
    """
    try:
        response = LLM_CLIENT.chat.completions.create(
            model="mistral-small",   
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a normal Indian person replying casually on chat. "
                        "Be short, natural, slightly curious. "
                        "Do NOT mention scams, money, links, or urgency."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            max_tokens=40
        )
        return response.choices[0].message.content.strip()

    except Exception:
        # absolute safety fallback
        return "Hello, kaun bol raha hai?"
