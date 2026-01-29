SESSION_MEMORY = {}

import time

def get_session(session_id: str):
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "scam_detected": False,
            "strategy_state": "HOOK",
            "start_time": time.time(),   # conversation start time
            "callback_sent": False,      # 👈 REQUIRED for GUVI callback
            "extracted": {
                "upi_ids": set(),
                "bank_accounts": set(),
                "phishing_urls": set(),
                "phone_numbers": set(),          # optional but future-safe
                "suspicious_keywords": set()     # optional but future-safe
            }
        }

    return SESSION_MEMORY[session_id]
