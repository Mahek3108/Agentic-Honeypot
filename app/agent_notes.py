def build_agent_notes(extracted: dict) -> str:
    notes = []

    if extracted.get("upi_ids"):
        notes.append("Asked for UPI payment")

    if extracted.get("bank_accounts"):
        notes.append("Shared bank account details")

    if extracted.get("phishing_urls"):
        notes.append("Sent phishing link")

    if extracted.get("phone_numbers"):
        notes.append("Used phone number to gain trust")

    if extracted.get("suspicious_keywords"):
        notes.append("Used urgency and threat-based language")

    if not notes:
        return "Used social engineering tactics"

    return "; ".join(notes)
