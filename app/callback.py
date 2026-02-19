
import requests
import logging
import time

GUVI_PRODUCTION_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
MY_PERSONAL_WEBHOOK = "https://viola-tetrabasic-elliptically.ngrok-free.dev/updateHoneyPotFinalResult"


def send_final_callback(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    extracted: dict,
    agent_notes: str,
    session_start_time: float
):
    """
    Sends final intelligence payload in UPDATED evaluation format.
    """

    duration_seconds = int(time.time() - session_start_time)

    payload = {
        "status": "success",
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "extractedIntelligence": {
            "bankAccounts": list(extracted.get("bank_accounts", [])),
            "upiIds": list(extracted.get("upi_ids", [])),
            "phoneNumbers": list(extracted.get("phone_numbers", [])),
            "phishingLinks": list(extracted.get("phishing_urls", [])),
            "emailAddresses": list(extracted.get("emails", [])), # ✅ FIXED
            "suspiciousKeywords": list(extracted.get("suspicious_keywords", []))
        },
        "engagementMetrics": {
            "engagementDurationSeconds": duration_seconds,
            "totalMessagesExchanged": total_messages
        },
        "agentNotes": agent_notes
    }

    logging.info(f"Final callback payload: {payload}")

    # Send to GUVI
    try:
        res = requests.post(
            GUVI_PRODUCTION_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        logging.info(f"GUVI callback status: {res.status_code}")
    except Exception as e:
        logging.error(f"GUVI callback failed: {e}")

    # Mirror to your webhook
    try:
        requests.post(
            MY_PERSONAL_WEBHOOK,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
    except Exception:
        pass

