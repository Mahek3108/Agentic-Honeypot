# import re

# SUSPICIOUS_KEYWORDS = [
#     "urgent", "immediately", "blocked", "suspended", "verify",
#     "verification", "compromised", "hacked", "otp", "account",
#     "freeze", "limited time"
# ]

# def extract_intelligence(text: str):
#     text_lower = text.lower()

#     # ---------- URLs ----------
#     url_pattern = r"http[s]?://\S+"

#     # ---------- UPI ----------
#     upi_pattern =  r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}\b"


#     # ---------- Phone Numbers ----------
#     phone_pattern = r"""
#         (?:
#             \+91[\s\-]?\d{10} |
#             91[\s\-]?\d{10} |
#             \b\d{10}\b
#         )
#     """

#     # ---------- Emails ----------
#     email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

#     # ---------- Extract first ----------
#     phones = set(re.findall(phone_pattern, text, flags=re.VERBOSE))
#     upis = set(re.findall(upi_pattern, text))
#     urls = set(re.findall(url_pattern, text))
#     emails = set(re.findall(email_pattern, text))
    
#     # ---------- Bank Accounts (EXCLUDE phones) ----------
#     bank_pattern = r"\b\d{11,18}\b"   # 👈 start from 11
#     raw_numbers = set(re.findall(bank_pattern, text))
#     bank_context_words = ["account", "bank", "a/c", "acc", "ifsc"]

#     bank_accounts = set()
#     if any(ctx in text_lower for ctx in bank_context_words):
#         bank_accounts = {
#             num for num in raw_numbers
#             if num not in phones
#         }
    

#     suspicious_found = [
#         kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
#     ]
#     upi_ids = set()
#     if "upi" in text_lower or "payment" in text_lower or "pay" in text_lower:
#         upi_ids = set(re.findall(upi_pattern, text))

#     # return {
#     #     "upi_ids": upi_ids,
#     #     "bank_accounts": set(re.findall(bank_pattern, text)),
#     #     "phishing_urls": set(re.findall(url_pattern, text)),
#     #     "phone_numbers": set(re.findall(phone_pattern, text)),
#     #     "suspicious_keywords": {
#     #         kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
#     #     },
#     #     "misc": {}
#     # }
#     return {
#         "upi_ids": upi_ids,
#         "bank_accounts": bank_accounts,
#         "phishing_urls": urls,
#         "phone_numbers": phones,
#         "emails": emails,
#         "suspicious_keywords": set(suspicious_found),
#         "misc": {}
#     }
import re

SUSPICIOUS_KEYWORDS = [
    "urgent", "immediately", "blocked", "suspended", "verify",
    "verification", "compromised", "hacked", "otp", "account",
    "freeze", "limited time", "kyc", "customer care", "unblock"
]

def extract_intelligence(text: str):
    if not text:
        return {k: [] for k in ["upi_ids", "bank_accounts", "phishing_urls", "phone_numbers", "emails", "suspicious_keywords"]}

    text_lower = text.lower()
    
    # 1. ---------- Emails (Strict: must have a dot after @) ----------
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = set(re.findall(email_pattern, text))

    # 2. ---------- UPI (Fixed: No dot allowed in the handle part) ----------
    # Ye pattern kehta hai: @ ke baad word characters hon, par unke baad koi dot (.) na ho
    upi_pattern = r"[a-zA-Z0-9.\-_]{3,}@[a-zA-Z]{3,}(?!\.[a-zA-Z]{2,})"
    raw_upis = set(re.findall(upi_pattern, text))
    # Filter: Jo email hai wo UPI nahi ho sakta
    upi_ids = {u for u in raw_upis if u not in emails}

    # 3. ---------- Phone Numbers ----------
    phone_pattern = r"(?:\+91|91)?[\s\-]?\d{10}"
    phones = set(re.findall(phone_pattern, text))
    # Comparison ke liye clean version (last 10 digits)
    clean_phones = {re.sub(r"\D", "", p)[-10:] for p in phones}

    # 4. ---------- Bank Accounts (Smart Context Filter) ----------
    bank_pattern = r"\b\d{11,18}\b"
    raw_numbers = set(re.findall(bank_pattern, text))
    
    bank_context_words = ["acc", "account", "a/c", "bank", "transfer", "ifsc", "beneficiary", "deposit"]
    bank_accounts = set()
    
    # Check if context suggests a bank account
    if any(ctx in text_lower for ctx in bank_context_words):
        for num in raw_numbers:
            # Bank account 10 digit ka phone nahi hona chahiye
            if num[-10:] not in clean_phones:
                bank_accounts.add(num)

    # 5. ---------- Phishing URLs ----------
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    urls = set(re.findall(url_pattern, text))

    # 6. ---------- Suspicious Keywords ----------
    suspicious_found = {kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower}

    # Sabko list mein convert karo for JSON compatibility
    return {
        "upi_ids": list(upi_ids),
        "bank_accounts": list(bank_accounts),
        "phishing_urls": list(urls),
        "phone_numbers": list(phones),
        "emails": list(emails),
        "suspicious_keywords": list(suspicious_found),
        "misc": {}
    }