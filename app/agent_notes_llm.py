from app.llm_client import call_llm

AGENT_NOTES_PROMPT = """
You are a cybersecurity analyst reviewing a scam conversation.

Write 1 concise sentence explaining:
- scammer tactics used
- intent (fraud, phishing, impersonation)
- behavioral patterns

Do NOT mention AI or analysis process.
Be professional and factual.
"""

def generate_agent_notes_llm(extracted: dict, last_message: str) -> str:
    context = f"""
Last scammer message:
"{last_message}"

Extracted intelligence:
UPI IDs: {list(extracted.get("upi_ids", []))}
Bank Accounts: {list(extracted.get("bank_accounts", []))}
Links: {list(extracted.get("phishing_urls", []))}
Phone Numbers: {list(extracted.get("phone_numbers", []))}
Suspicious Keywords: {list(extracted.get("suspicious_keywords", []))}
"""

    try:
        return call_llm(
            system_prompt=AGENT_NOTES_PROMPT,
            user_prompt=context,
            temperature=0.4
        )
    except Exception:
        return "Scammer used social engineering and urgency-based tactics."
