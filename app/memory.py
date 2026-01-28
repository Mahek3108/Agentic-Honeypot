SESSION_MEMORY = {}

import time
def get_session(session_id: str):
    if session_id not in SESSION_MEMORY:
        # SESSION_MEMORY[session_id] = {
        #     "scam_detected": False,
        #     "extracted": {
        #         "upi_ids": set(),
        #         "bank_accounts": set(),
        #         "phishing_urls": set()
        #     }
        # }
        SESSION_MEMORY[session_id] = {
    "scam_detected": False,
    "strategy_state": "HOOK",
    "start_time": time.time(),   # 👈 conversation start
    "extracted": {
        "upi_ids": set(),
        "bank_accounts": set(),
        "phishing_urls": set()
    }
}

    return SESSION_MEMORY[session_id]
