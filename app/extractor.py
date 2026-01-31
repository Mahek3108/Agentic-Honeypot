import re

SUSPICIOUS_KEYWORDS = [
    "urgent", "immediately", "blocked", "suspended", "verify",
    "verification", "compromised", "hacked", "otp", "account",
    "freeze", "limited time"
]

def extract_intelligence(text: str):
    text_lower = text.lower()

    # ---------- URLs ----------
    url_pattern = r"http[s]?://\S+"

    # ---------- UPI ----------
    upi_pattern =  r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}\b"


    # ---------- Phone Numbers ----------
    phone_pattern = r"""
        (?:
            \+91[\s\-]?\d{10} |
            91[\s\-]?\d{10} |
            \b\d{10}\b
        )
    """

    # ---------- Emails ----------
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    # ---------- Extract first ----------
    phones = set(re.findall(phone_pattern, text, flags=re.VERBOSE))
    upis = set(re.findall(upi_pattern, text))
    urls = set(re.findall(url_pattern, text))
    emails = set(re.findall(email_pattern, text))
    
    # ---------- Bank Accounts (EXCLUDE phones) ----------
    bank_pattern = r"\b\d{11,18}\b"   # 👈 start from 11
    raw_numbers = set(re.findall(bank_pattern, text))
    bank_context_words = ["account", "bank", "a/c", "acc", "ifsc"]

    bank_accounts = set()
    if any(ctx in text_lower for ctx in bank_context_words):
        bank_accounts = {
            num for num in raw_numbers
            if num not in phones
        }
    

    suspicious_found = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
    ]
    upi_ids = set()
    if "upi" in text_lower or "payment" in text_lower or "pay" in text_lower:
        upi_ids = set(re.findall(upi_pattern, text))

    # return {
    #     "upi_ids": upi_ids,
    #     "bank_accounts": set(re.findall(bank_pattern, text)),
    #     "phishing_urls": set(re.findall(url_pattern, text)),
    #     "phone_numbers": set(re.findall(phone_pattern, text)),
    #     "suspicious_keywords": {
    #         kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
    #     },
    #     "misc": {}
    # }
    return {
        "upi_ids": upi_ids,
        "bank_accounts": bank_accounts,
        "phishing_urls": urls,
        "phone_numbers": phones,
        "emails": emails,
        "suspicious_keywords": set(suspicious_found),
        "misc": {}
    }
