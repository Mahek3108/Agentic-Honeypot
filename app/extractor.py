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
    upi_pattern = r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b"

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

    bank_accounts = {
        num for num in raw_numbers
        if num not in phones
    }

    suspicious_found = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
    ]

    return {
        "upi_ids": upis,
        "bank_accounts": bank_accounts,
        "phishing_urls": urls,
        "phone_numbers": phones,
        "emails": emails,
        "suspicious_keywords": set(suspicious_found),
        "misc": {}
    }
