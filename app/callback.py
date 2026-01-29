# app/callback.py
import requests
import logging

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    extracted: dict,
    agent_notes: str = ""
):
    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": {
            "bankAccounts": list(extracted.get("bank_accounts", [])),
            "upiIds": list(extracted.get("upi_ids", [])),
            "phishingLinks": list(extracted.get("phishing_urls", [])),
            "phoneNumbers": list(extracted.get("phone_numbers", [])),
            "suspiciousKeywords": list(extracted.get("suspicious_keywords", []))
        },
        "agentNotes": agent_notes
    }

    try:
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
        logging.info(
            f"GUVI callback sent | status={response.status_code} | session={session_id}"
        )
    except Exception as e:
        logging.error(f"GUVI callback failed | session={session_id} | error={e}")
