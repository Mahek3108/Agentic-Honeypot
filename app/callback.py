# # # app/callback.py

# import requests
# import logging

# GUVI_CALLBACK_URL = "https://webhook.site/e490e5f9-ed4b-46d2-acf6-8542108371db"


# def send_final_callback(
#     session_id: str,
#     scam_detected: bool,
#     total_messages: int,
#     extracted: dict,
#     agent_notes: str
# ):
#     """
#     Sends final intelligence payload to GUVI evaluation endpoint.
#     Must be called ONLY ONCE per session.
#     """

#     payload = {
#     "sessionId": session_id,
#     "scamDetected": scam_detected,
#     "totalMessagesExchanged": total_messages,
#     "extractedIntelligence": {
#         "bankAccounts": list(extracted.get("bank_accounts", [])),
#         "upiIds": list(extracted.get("upi_ids", [])),
#         "phishingLinks": list(extracted.get("phishing_urls", [])), # Section 12 key name
#         "phoneNumbers": list(extracted.get("phone_numbers", [])),   # Section 12 key name
#         "suspiciousKeywords": list(extracted.get("suspicious_keywords", []))
#     },
#     "agentNotes": agent_notes
# }

#     logging.info(
#         f"Sending GUVI callback | session={session_id} | messages={total_messages}"
#     )

#     # 🔹 Retry once if network hiccup
#     for attempt in range(2):
#         try:
#             response = requests.post(
#                 GUVI_CALLBACK_URL,
#                 json=payload,
#                 headers={"Content-Type": "application/json"},
#                 timeout=5
#             )

#             logging.info(
#                 f"GUVI callback success | status={response.status_code} | session={session_id}"
#             )
#             break

#         except Exception as e:
#             logging.error(
#                 f"GUVI callback failed (attempt {attempt + 1}) | "
#                 f"session={session_id} | error={e}"
#             )
import requests
import logging

# 1. GUVI ka Fixed Endpoint (Jahan marks milenge)
GUVI_PRODUCTION_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# 2. Tera Personal Webhook (Jahan tum live check karoge)
MY_PERSONAL_WEBHOOK = "https://viola-tetrabasic-elliptically.ngrok-free.dev/updateHoneyPotFinalResult"

def send_final_callback(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    extracted: dict,
    agent_notes: str
):
    """
    Sends final intelligence payload to BOTH GUVI and Personal Webhook.
    """

    # Payload as per Section 12 (CamelCase Keys)
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

    logging.info(f"Initiating callbacks for session={session_id}")

    # --- ACTION 1: Send to GUVI Production ---
    for attempt in range(2):
        try:
            res = requests.post(
                GUVI_PRODUCTION_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            logging.info(f"GUVI Production success | status={res.status_code}")
            break
        except Exception as e:
            logging.error(f"GUVI Production failed (attempt {attempt + 1}): {e}")

    # --- ACTION 2: Mirror to Personal Webhook (For your tracking) ---
    try:
        requests.post(
            MY_PERSONAL_WEBHOOK,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        logging.info("Mirror copy sent to Webhook.site successfully.")
    except Exception as e:
        logging.error(f"Mirroring to Webhook failed: {e}")
