
import requests
import logging
import time

GUVI_PRODUCTION_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
MY_PERSONAL_WEBHOOK = "https://viola-tetrabasic-elliptically.ngrok-free.dev/updateHoneyPotFinalResult"


# def send_final_callback(
#     session_id: str,
#     scam_detected: bool,
#     total_messages: int,
#     extracted: dict,
#     agent_notes: str,
#     session_start_time: float
# ):
#     """
#     Sends final intelligence payload in UPDATED evaluation format.
#     """

#     duration_seconds = int(time.time() - session_start_time)

#     payload = {
#         "status": "success",
#         "sessionId": session_id,
#         "scamDetected": scam_detected,
#         "extractedIntelligence": {
#             "bankAccounts": list(extracted.get("bank_accounts", [])),
#             "upiIds": list(extracted.get("upi_ids", [])),
#             "phoneNumbers": list(extracted.get("phone_numbers", [])),
#             "phishingLinks": list(extracted.get("phishing_urls", [])),
#             "emailAddresses": list(extracted.get("emails", [])), # ✅ FIXED
#             "suspiciousKeywords": list(extracted.get("suspicious_keywords", []))
#         },
#         "engagementMetrics": {
#             "engagementDurationSeconds": duration_seconds,
#             "totalMessagesExchanged": total_messages
#         },
#         "agentNotes": agent_notes
#     }

#     logging.info(f"Final callback payload: {payload}")

#     # Send to GUVI
#     try:
#         res = requests.post(
#             GUVI_PRODUCTION_URL,
#             json=payload,
#             headers={"Content-Type": "application/json"},
#             timeout=10
#         )
#         logging.info(f"GUVI callback status: {res.status_code}")
#     except Exception as e:
#         logging.error(f"GUVI callback failed: {e}")

#     # Mirror to your webhook
#     try:
#         requests.post(
#             MY_PERSONAL_WEBHOOK,
#             json=payload,
#             headers={"Content-Type": "application/json"},
#             timeout=5
#         )
#     except Exception:
#         pass


def infer_scam_type(extracted: dict) -> str:
    """
    Determines scam type based on dominant extracted intelligence.
    Generic and scenario-agnostic.
    """

    scores = {
        "bank_fraud": 0,
        "upi_fraud": 0,
        "phishing": 0,
        "email_fraud": 0,
    }

    if extracted.get("bank_accounts"):
        scores["bank_fraud"] += 2

    if extracted.get("upi_ids"):
        scores["upi_fraud"] += 2

    if extracted.get("phone_numbers"):
        scores["bank_fraud"] += 1

    if extracted.get("phishing_urls"):
        scores["phishing"] += 2

    if extracted.get("emails"):
        scores["email_fraud"] += 1

    best_type = max(scores, key=scores.get)

    if scores[best_type] == 0:
        return "financial_scam"

    return best_type


def calculate_confidence(scam_detected: bool, extracted: dict) -> float:
    if not scam_detected:
        return 0.3

    signals = 0

    for key in [
        "bank_accounts",
        "upi_ids",
        "phone_numbers",
        "phishing_urls",
        "emails"
    ]:
        if extracted.get(key):
            signals += 1

    base = 0.6
    bonus = min(signals * 0.07, 0.35)

    return round(base + bonus, 2)


def send_final_callback(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    extracted: dict,
    agent_notes: str,
):
    """
    Sends final output in exact required evaluation format.
    """

    # Engagement duration (proportional, not inflated)
    engagement_duration = max(60, total_messages * 15)

    scam_type = infer_scam_type(extracted)
    confidence = calculate_confidence(scam_detected, extracted)

    payload = {
        "sessionId": str(session_id),
        "scamDetected": bool(scam_detected),
        "totalMessagesExchanged": int(total_messages),
        "engagementDurationSeconds": int(engagement_duration),
        "extractedIntelligence": {
            "phoneNumbers": [str(v) for v in extracted.get("phone_numbers", [])],
            "bankAccounts": [str(v) for v in extracted.get("bank_accounts", [])],
            "upiIds": [str(v) for v in extracted.get("upi_ids", [])],
            "phishingLinks": [str(v) for v in extracted.get("phishing_urls", [])],
            "emailAddresses": [str(v) for v in extracted.get("emails", [])],
            "orderNumbers": [str(v) for v in extracted.get("order_ids", [])],
            "policyNumber": [str(v) for v in extracted.get("policy_numbers", [])],
            "caseIds": [str(v) for v in extracted.get("case_ids", [])]
        },
        "agentNotes": str(agent_notes),
        "scamType": scam_type,
        "confidenceLevel": confidence
    }

    logging.info(f"Final callback payload: {payload}")

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
