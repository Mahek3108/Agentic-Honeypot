SESSION_MEMORY = {}

import time

def get_session(session_id: str):
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "scam_detected": False,
            "strategy_state": "HOOK",
            "start_time": time.time(),
            "callback_sent": False,
            "process_status": "started",
            "messages_exchanged": 0,
            "extracted": {
                "upi_ids": set(),
                "bank_accounts": set(),
                "phishing_urls": set(),
                "phone_numbers": set(),
                "suspicious_keywords": set(),
                "emails": set(),
                "order_ids": set(),
                "policy_numbers": set(),
                "case_ids": set(),
        
                "misc": {}
            }
        }
    return SESSION_MEMORY[session_id]
