# # app/callback.py

import requests
import logging

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"


def send_final_callback(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    extracted: dict,
    agent_notes: str
):
    """
    Sends final intelligence payload to GUVI evaluation endpoint.
    Must be called ONLY ONCE per session.
    """

    # callback.py mein check karein ki keys exactly yehi hon:
    payload = {
    "sessionId": session_id,
    "scamDetected": scam_detected,
    "totalMessagesExchanged": total_messages,
    "extractedIntelligence": {
        "bankAccounts": list(extracted.get("bank_accounts", [])),
        "upiIds": list(extracted.get("upi_ids", [])),
        "phishingLinks": list(extracted.get("phishing_urls", [])), # Section 12 key name
        "phoneNumbers": list(extracted.get("phone_numbers", [])),   # Section 12 key name
        "suspiciousKeywords": list(extracted.get("suspicious_keywords", []))
    },
    "agentNotes": agent_notes
}

    # 🔹 Optional: log payload size (not full payload)
    logging.info(
        f"Sending GUVI callback | session={session_id} | messages={total_messages}"
    )

    # 🔹 Retry once if network hiccup
    for attempt in range(2):
        try:
            response = requests.post(
                GUVI_CALLBACK_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            logging.info(
                f"GUVI callback success | status={response.status_code} | session={session_id}"
            )
            break

        except Exception as e:
            logging.error(
                f"GUVI callback failed (attempt {attempt + 1}) | "
                f"session={session_id} | error={e}"
            )
