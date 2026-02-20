
import re

SUSPICIOUS_KEYWORDS = [
    "urgent", "immediately", "blocked", "suspended", "verify",
    "verification", "compromised", "hacked", "otp", "account",
    "freeze", "limited time", "kyc", "customer care", "unblock",
    "lottery", "cashback", "reward", "pancard"
]

def extract_intelligence(text: str):

    if not text:
        return {
            "upi_ids": [],
            "bank_accounts": [],
            "phishing_urls": [],
            "phone_numbers": [],
            "emails": [],
            "order_ids": [],
            "policy_numbers": [],
            "case_ids": [],
            "suspicious_keywords": [],
            "red_flags":[],
            "misc": {}
        }

    text_lower = text.lower()

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    emails = set(re.findall(email_pattern, text))

    upi_pattern = r"\b[A-Za-z0-9._-]{2,}@[A-Za-z0-9]{2,}\b"
    potential_upis = set(re.findall(upi_pattern, text))

    upi_ids = set()

    for u in potential_upis:
        
        if any(u in e for e in emails):
            continue
        upi_ids.add(u)

    bank_pattern = r"\b\d{11,18}\b"
    raw_bank_numbers = set(re.findall(bank_pattern, text))

    bank_context_words = [
        "bank", "account", "acc", "a/c",
        "transfer", "ifsc", "beneficiary", "deposit"
    ]

    bank_accounts = []

    if any(ctx in text_lower for ctx in bank_context_words):
        bank_accounts = list(raw_bank_numbers)

    # -------------------------
    # 4. PHONE NUMBERS (Indian)
    # -------------------------
    # phone_pattern = r"(?:\+91|91)?[-\s]?[6789]\d{9}\b"
    # raw_phones = re.findall(phone_pattern, text)

    # final_phones = set()

    # for p in raw_phones:
    #     clean_p = re.sub(r"\D", "", p)[-10:]

    #     # avoid phone inside bank account
    #     if not any(clean_p in b for b in raw_bank_numbers):
    #         final_phones.add(p)
    

    # phone_pattern = r"""
    # (
    #     (?:\+91[\-\s]?)?[6-9]\d{9}              # Indian mobile
    #     |
    #     1800[\-\s]?\d{3}[\-\s]?\d{4}            # Toll-free 1800
    #     |
    #     \b\d{3,4}[\-\s]\d{3}[\-\s]\d{4}\b       # 000-000-0000 style
    # )
    # """

    # raw_phones = re.findall(phone_pattern, text, flags=re.VERBOSE)

    # final_phones = set()

    # for p in raw_phones:
    #     clean_p = re.sub(r"\D", "", p)

    #     # Avoid phone inside bank account
    #     if not any(clean_p in b for b in raw_bank_numbers):
    #         final_phones.add(p.strip())
    phone_pattern = r"""
        (?:\+91[-\s]?)?[6-9]\d{9}\b                     # Mobile with or without +91
        |
        \b[6-9]\d{9}\b                                  # Plain 10 digit mobile
        |
        \b1\d{3}[-\s]?\d{3,4}[-\s]?\d{3,4}\b            # Toll free 4-3-3 / 4-3-4 / 4-4-4
        |
        \b0\d{2,4}[-\s]?\d{6,8}\b                       # Landline STD codes
        """

    raw_phones = re.findall(phone_pattern, text, flags=re.VERBOSE)

    final_phones = set()

    for p in raw_phones:
        clean_p = re.sub(r"\D", "", p)

        # avoid overlap with bank account numbers
        if not any(clean_p in b for b in raw_bank_numbers):
            final_phones.add(p.strip())
    # -------------------------
    # 5. URLS (Phishing)
    # -------------------------
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    urls = set(re.findall(url_pattern, text))

    # -------------------------
    # 6. POLICY / ORDER / CASE
    # Bidirectional window logic
    # -------------------------

    policy_numbers = set()
    order_ids = set()
    case_ids = set()

    words = text.split()

    def is_valid_id(token):
        clean = re.sub(r"[^A-Za-z0-9\-]", "", token)
        return (
            len(clean) >= 4 and
            any(c.isdigit() for c in clean)
        )

    for i, word in enumerate(words):
        lw = word.lower()

        # window: 2 words before, 5 words after
        start = max(0, i - 2)
        end = min(len(words), i + 6)
        window = words[start:end]

        for token in window:
            clean_token = re.sub(r"[^A-Za-z0-9\-]", "", token)

            if not is_valid_id(clean_token):
                continue

            if "policy" in lw:
                policy_numbers.add(clean_token)
                break

            elif "order" in lw:
                order_ids.add(clean_token)
                break

            elif "case" in lw:
                case_ids.add(clean_token)
                break

    # -------------------------
    # 7. SUSPICIOUS KEYWORDS
    # -------------------------
    suspicious_found = {
        kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
    }

    # -------------------------
    # FINAL STRUCTURED OUTPUT
    # -------------------------

    return {
        "upi_ids": list(upi_ids),
        "bank_accounts": list(bank_accounts),
        "phishing_urls": list(urls),
        "phone_numbers": list(final_phones),
        "emails": list(emails),
        "order_ids": list(order_ids),
        "policy_numbers": list(policy_numbers),
        "case_ids": list(case_ids),
        "suspicious_keywords": list(suspicious_found),
        "red_flags": list(suspicious_found),
        "misc": {}
    }