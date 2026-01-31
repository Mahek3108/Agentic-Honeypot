import re

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "immediately",
    "blocked",
    "suspended",
    "verify",
    "verification",
    "compromised",
    "hacked",
    "otp",
    "account",
    "freeze",
    "limited time"
]


def extract_intelligence(text: str):
    text_lower = text.lower()

    # ---------- UPI IDs ----------
    upi_pattern = r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b"

    # ---------- Bank Account Numbers ----------
    # 9–18 digits, standalone
    bank_pattern = r"\b\d{9,18}\b"

    # ---------- URLs ----------
    url_pattern = r"http[s]?://\S+"

    # ---------- Phone Numbers ----------
    # Covers:
    # +91XXXXXXXXXX
    # 91XXXXXXXXXX
    # XXXXXXXXXX
    # XXX XXX XXXX
    phone_pattern = r"""
        (?:
            \+?\d{1,3}[\s\-]?
        )?
        \b\d{10}\b
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    emails = set(re.findall(email_pattern, text))

    # ---------- Suspicious Keywords ----------
    suspicious_found = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
    ]

    return {
        "upi_ids": set(re.findall(upi_pattern, text)),
        "bank_accounts": set(re.findall(bank_pattern, text)),
        "phishing_urls": set(re.findall(url_pattern, text)),
        "phone_numbers": set(re.findall(phone_pattern, text, flags=re.VERBOSE)),
        "suspicious_keywords": set(suspicious_found),
        "emails": emails,
        "misc": {}
}
