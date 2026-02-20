
# # import re

# # SUSPICIOUS_KEYWORDS = [
# #     "urgent", "immediately", "blocked", "suspended", "verify",
# #     "verification", "compromised", "hacked", "otp", "account",
# #     "freeze", "limited time", "kyc", "customer care", "unblock"
# # ]

# # def extract_intelligence(text: str):
# #     if not text:
# #         return {
# #             "upi_ids": [],
# #             "bank_accounts": [],
# #             "phishing_urls": [],
# #             "phone_numbers": [],
# #             "emails": [],
# #             "order_ids": [],
# #             "policy_numbers": [],
# #             "case_ids": [],
# #             "suspicious_keywords": [],
# #             "misc": {}
# #         }

# #     text_lower = text.lower()
    
# #     # 1 Emails
# #     email_pattern = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
# #     emails = set(re.findall(email_pattern, text))

# #     # 2.UPI 
# #     raw_upi_pattern = r"[\w\.-]+@[\w\.-]+"
# #     potential_upis = re.findall(raw_upi_pattern, text)
    
# #     upi_ids = []
# #     for candidate in potential_upis:
# #         candidate_lower = candidate.lower().strip()
# #         if "@" in candidate_lower:
# #             parts = candidate_lower.split("@")
# #             handle_part = parts[1] if len(parts) > 1 else ""
            
# #             if "." not in handle_part:
# #                 if not any(candidate_lower in e.lower() for e in emails):
# #                     upi_ids.append(candidate)

# #     # 3.bank accounts
# #     bank_pattern = r"\b\d{11,18}\b"
# #     raw_bank_numbers = set(re.findall(bank_pattern, text))

# #     # 4. Phone Numbers 
    
# #     phone_pattern = r"(?:\+91|91)?[\s\-]?\b\d{10}\b" 
# #     found_phones = set(re.findall(phone_pattern, text))
    
    
# #     final_phones = []
# #     for p in found_phones:
# #         clean_p = re.sub(r"\D", "", p)[-10:]
        
# #         if not any(clean_p in b for b in raw_bank_numbers):
# #             final_phones.append(p)

# #     bank_context_words = ["acc", "account", "a/c", "bank", "transfer", "ifsc", "beneficiary", "deposit"]
# #     bank_accounts = []
# #     if any(ctx in text_lower for ctx in bank_context_words):
# #         bank_accounts = list(raw_bank_numbers)


# #     # order_pattern = r"(?:order\s*(?:id|number)?[:\-\s]+)([A-Za-z0-9\-]{5,})"
# #     # order_ids=set(re.findall(order_pattern,text, flags=re.IGNORECASE))

# #     # policy_pattern = r"(?:policy\s*{?:no|number)?[:\-\s]+)([A-Za-z0-9\-]{5,})"
# #     # policy_numbers= set(re.findall(policy_pattern, text, flags=re.IGNORECASE))

# #     # case_pattern = r"(?:case\s*(?:id|number)?[:\-\s]+)([A-Za-z0-9\-](5,})"
# #     # case_ids = set(re.findall(case_pattern, text, flags= re.IGNORECASE))
# #     # 5. url
# #     url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
# #     urls = set(re.findall(url_pattern, text))

# #     order_ids = set()
# #     policy_numbers = set()
# #     case_ids = set()

# #     lines = text.splitlines()

# #     for line in lines:
# #         lower_line = line.lower()
# #         tokens = re.findall(r"\b[A-Za-z0-9\-]{4,}\b", line)

# #         for token in tokens:
# #             if token.isdigit() and len(token) < 4:
# #                 continue

# #             if "order" in lower_line:
# #                 order_ids.add(token)

# #             elif "policy" in lower_line:
# #                 policy_numbers.add(token)

# #             elif "case" in lower_line:
# #                 case_ids.add(token)

# #     bank_set = set(bank_accounts)

# #     order_ids -= bank_set
# #     policy_numbers -= bank_set
# #     case_ids -= bank_set

# #     policy_numbers -= order_ids
# #     case_ids -= order_ids
# #     case_ids -= policy_numbers


# #     # 6. Suspicious Keywords 
# #     suspicious_found = {kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower}

# #     return {
# #         "upi_ids": list(upi_ids),
# #         "bank_accounts": list(bank_accounts),
# #         "phishing_urls": list(urls),
# #         "phone_numbers": list(set(final_phones)),
# #         "emails": list(emails),
# #         "order_ids": list(order_ids),
# #         "policy_numbers": list(policy_numbers),
# #         "case_ids": list(case_ids),
# #         "suspicious_keywords": list(suspicious_found),
# #         "misc": {}
# #     }
# import re

# SUSPICIOUS_KEYWORDS = [
#     "urgent", "immediately", "blocked", "suspended", "verify",
#     "verification", "compromised", "hacked", "otp", "account",
#     "freeze", "limited time", "kyc", "customer care", "unblock"
# ]

# def extract_intelligence(text: str):

#     if not text:
#         return {
#             "upi_ids": [],
#             "bank_accounts": [],
#             "phishing_urls": [],
#             "phone_numbers": [],
#             "emails": [],
#             "order_ids": [],
#             "policy_numbers": [],
#             "case_ids": [],
#             "suspicious_keywords": [],
#             "misc": {}
#         }

#     text_lower = text.lower()

#     # -------------------------
#     # 1. EMAILS
#     # -------------------------
#     email_pattern = r"\b[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}\b"
#     emails = set(re.findall(email_pattern, text))

#     # -------------------------
#     # 2. UPI IDs (exclude emails)
#     # -------------------------
#     raw_upi_pattern = r"\b[\w\.-]+@[\w\.-]+\b"
#     potential_upis = re.findall(raw_upi_pattern, text)

#     upi_ids = set()

#     for candidate in potential_upis:
#         candidate_lower = candidate.lower().strip()

#         if candidate_lower in [e.lower() for e in emails]:
#             continue

#         parts = candidate_lower.split("@")
#         if len(parts) == 2 and "." not in parts[1]:
#             upi_ids.add(candidate)

#     # -------------------------
#     # 3. BANK ACCOUNTS (11–18 digits)
#     # -------------------------
#     bank_pattern = r"\b\d{11,18}\b"
#     raw_bank_numbers = set(re.findall(bank_pattern, text))

#     bank_context_words = [
#         "acc", "account", "a/c", "bank",
#         "transfer", "ifsc", "beneficiary", "deposit"
#     ]

#     bank_accounts = []

#     if any(ctx in text_lower for ctx in bank_context_words):
#         bank_accounts = list(raw_bank_numbers)

#     # -------------------------
#     # 4. PHONE NUMBERS (India)
#     # -------------------------
#     phone_pattern = r"(?:\+91|91)?[\s\-]?\b\d{10}\b"
#     found_phones = set(re.findall(phone_pattern, text))

#     final_phones = set()

#     for p in found_phones:
#         clean_p = re.sub(r"\D", "", p)[-10:]

#         # avoid bank account overlap
#         if not any(clean_p in b for b in raw_bank_numbers):
#             final_phones.add(p)

#     # -------------------------
#     # 5. URLS
#     # -------------------------
#     url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
#     urls = set(re.findall(url_pattern, text))

#     # -------------------------
#     # 6. ORDER / POLICY / CASE IDS
#     # Strict context + digit required
#     # -------------------------

#     policy_pattern = r"policy\s*(?:id|no|number)?\s*(?:is|:|-)?\s*([A-Za-z0-9\-]*\d[A-Za-z0-9\-]{3,})"
#     order_pattern  = r"order\s*(?:id|number)?\s*(?:is|:|-)?\s*([A-Za-z0-9\-]*\d[A-Za-z0-9\-]{3,})"
#     case_pattern   = r"case\s*(?:id|number)?\s*(?:is|:|-)?\s*([A-Za-z0-9\-]*\d[A-Za-z0-9\-]{3,})"

#     policy_numbers = set(re.findall(policy_pattern, text, flags=re.IGNORECASE))
#     order_ids = set(re.findall(order_pattern, text, flags=re.IGNORECASE))
#     case_ids = set(re.findall(case_pattern, text, flags=re.IGNORECASE))

#     # -------------------------
#     # 7. SUSPICIOUS KEYWORDS
#     # -------------------------
#     suspicious_found = {
#         kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
#     }

#     # -------------------------
#     # FINAL STRUCTURED OUTPUT
#     # -------------------------

#     return {
#         "upi_ids": list(upi_ids),
#         "bank_accounts": list(bank_accounts),
#         "phishing_urls": list(urls),
#         "phone_numbers": list(final_phones),
#         "emails": list(emails),
#         "order_ids": list(order_ids),
#         "policy_numbers": list(policy_numbers),
#         "case_ids": list(case_ids),
#         "suspicious_keywords": list(suspicious_found),
#         "misc": {}
#     }
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

    # -------------------------
    # 1. EMAILS
    # -------------------------
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    emails = set(re.findall(email_pattern, text))

    # -------------------------
    # 2. UPI IDS (email-safe)
    # -------------------------
    upi_pattern = r"\b[a-zA-Z0-9._\-]{2,256}@[a-zA-Z]{2,64}\b"
    potential_upis = re.findall(upi_pattern, text)

    upi_ids = {
        u for u in potential_upis
        if u not in emails
    }

    # -------------------------
    # 3. BANK ACCOUNTS (11–18 digits, context aware)
    # -------------------------
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
    

    phone_pattern = r"""
    (
        (?:\+91[\-\s]?)?[6-9]\d{9}              # Indian mobile
        |
        1800[\-\s]?\d{3}[\-\s]?\d{4}            # Toll-free 1800
        |
        \b\d{3,4}[\-\s]\d{3}[\-\s]\d{4}\b       # 000-000-0000 style
    )
    """

    raw_phones = re.findall(phone_pattern, text, flags=re.VERBOSE)

    final_phones = set()

    for p in raw_phones:
        clean_p = re.sub(r"\D", "", p)

        # Avoid phone inside bank account
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