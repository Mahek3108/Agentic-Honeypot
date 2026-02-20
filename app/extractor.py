# # # # import re

# # # # SUSPICIOUS_KEYWORDS = [
# # # #     "urgent", "immediately", "blocked", "suspended", "verify",
# # # #     "verification", "compromised", "hacked", "otp", "account",
# # # #     "freeze", "limited time"
# # # # ]

# # # # def extract_intelligence(text: str):
# # # #     text_lower = text.lower()

# # # #     # ---------- URLs ----------
# # # #     url_pattern = r"http[s]?://\S+"

# # # #     # ---------- UPI ----------
# # # #     upi_pattern =  r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}\b"


# # # #     # ---------- Phone Numbers ----------
# # # #     phone_pattern = r"""
# # # #         (?:
# # # #             \+91[\s\-]?\d{10} |
# # # #             91[\s\-]?\d{10} |
# # # #             \b\d{10}\b
# # # #         )
# # # #     """

# # # #     # ---------- Emails ----------
# # # #     email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# # # #     # ---------- Extract first ----------
# # # #     phones = set(re.findall(phone_pattern, text, flags=re.VERBOSE))
# # # #     upis = set(re.findall(upi_pattern, text))
# # # #     urls = set(re.findall(url_pattern, text))
# # # #     emails = set(re.findall(email_pattern, text))
    
# # # #     # ---------- Bank Accounts (EXCLUDE phones) ----------
# # # #     bank_pattern = r"\b\d{11,18}\b"   # 👈 start from 11
# # # #     raw_numbers = set(re.findall(bank_pattern, text))
# # # #     bank_context_words = ["account", "bank", "a/c", "acc", "ifsc"]

# # # #     bank_accounts = set()
# # # #     if any(ctx in text_lower for ctx in bank_context_words):
# # # #         bank_accounts = {
# # # #             num for num in raw_numbers
# # # #             if num not in phones
# # # #         }
    

# # # #     suspicious_found = [
# # # #         kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
# # # #     ]
# # # #     upi_ids = set()
# # # #     if "upi" in text_lower or "payment" in text_lower or "pay" in text_lower:
# # # #         upi_ids = set(re.findall(upi_pattern, text))

# # # #     # return {
# # # #     #     "upi_ids": upi_ids,
# # # #     #     "bank_accounts": set(re.findall(bank_pattern, text)),
# # # #     #     "phishing_urls": set(re.findall(url_pattern, text)),
# # # #     #     "phone_numbers": set(re.findall(phone_pattern, text)),
# # # #     #     "suspicious_keywords": {
# # # #     #         kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
# # # #     #     },
# # # #     #     "misc": {}
# # # #     # }
# # # #     return {
# # # #         "upi_ids": upi_ids,
# # # #         "bank_accounts": bank_accounts,
# # # #         "phishing_urls": urls,
# # # #         "phone_numbers": phones,
# # # #         "emails": emails,
# # # #         "suspicious_keywords": set(suspicious_found),
# # # #         "misc": {}
# # # #     }
# # # import re

# # # SUSPICIOUS_KEYWORDS = [
# # #     "urgent", "immediately", "blocked", "suspended", "verify",
# # #     "verification", "compromised", "hacked", "otp", "account",
# # #     "freeze", "limited time", "kyc", "customer care", "unblock"
# # # ]

# # # def extract_intelligence(text: str):
# # #     if not text:
# # #         return {k: [] for k in ["upi_ids", "bank_accounts", "phishing_urls", "phone_numbers", "emails", "suspicious_keywords"]}

# # #     text_lower = text.lower()
    
# # #     # 1. ---------- Emails (Strict: must have a dot after @) ----------
# # #     email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
# # #     emails = set(re.findall(email_pattern, text))

# # #     # 2. ---------- UPI (Fixed: No dot allowed in the handle part) ----------
# # #     # Ye pattern kehta hai: @ ke baad word characters hon, par unke baad koi dot (.) na ho
# # #     upi_pattern = r"[a-zA-Z0-9.\-_]{3,}@[a-zA-Z]{3,}(?!\.[a-zA-Z]{2,})"
# # #     raw_upis = set(re.findall(upi_pattern, text))
# # #     # Filter: Jo email hai wo UPI nahi ho sakta
# # #     upi_ids = {u for u in raw_upis if u not in emails}

# # #     # 3. ---------- Phone Numbers ----------
# # #     phone_pattern = r"(?:\+91|91)?[\s\-]?\d{10}"
# # #     phones = set(re.findall(phone_pattern, text))
# # #     # Comparison ke liye clean version (last 10 digits)
# # #     clean_phones = {re.sub(r"\D", "", p)[-10:] for p in phones}

# # #     # 4. ---------- Bank Accounts (Smart Context Filter) ----------
# # #     bank_pattern = r"\b\d{11,18}\b"
# # #     raw_numbers = set(re.findall(bank_pattern, text))
    
# # #     bank_context_words = ["acc", "account", "a/c", "bank", "transfer", "ifsc", "beneficiary", "deposit"]
# # #     bank_accounts = set()
    
# # #     # Check if context suggests a bank account
# # #     if any(ctx in text_lower for ctx in bank_context_words):
# # #         for num in raw_numbers:
# # #             # Bank account 10 digit ka phone nahi hona chahiye
# # #             if num[-10:] not in clean_phones:
# # #                 bank_accounts.add(num)

# # #     # 5. ---------- Phishing URLs ----------
# # #     url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
# # #     urls = set(re.findall(url_pattern, text))

# # #     # 6. ---------- Suspicious Keywords ----------
# # #     suspicious_found = {kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower}

# # #     # Sabko list mein convert karo for JSON compatibility
# # #     return {
# # #         "upi_ids": list(upi_ids),
# # #         "bank_accounts": list(bank_accounts),
# # #         "phishing_urls": list(urls),
# # #         "phone_numbers": list(phones),
# # #         "emails": list(emails),
# # #         "suspicious_keywords": list(suspicious_found),
# # #         "misc": {}
# # #     }
# # import re

# # def extract_intelligence(text: str):
# #     if not text:
# #         return {k: [] for k in ["upi_ids", "bank_accounts", "phishing_urls", "phone_numbers", "emails", "suspicious_keywords"]}

# #     text_lower = text.lower()
    
# #     # 1. ---------- Emails (Hyphen & Multiple Dots Safe) ----------
# #     # Purana: [a-zA-Z0-9._%+-]+ 
# #     # Naya: [\w\.-]+ (Ye hyphen '-' aur dot '.' dono ko handle karega)
# #     email_pattern = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
# #     emails = set(re.findall(email_pattern, text))

# #     # 2. ---------- UPI (Strict Anti-Email Logic) ----------
# #     # Pattern: @ ke baad word chars ya hyphen ho, par koi dot (.) na ho
# #     upi_pattern = r"[\w\.-]+@[\w-]{3,}(?!\.[a-zA-Z]{2,})"
# #     all_possible_upis = set(re.findall(upi_pattern, text))

# #     # Cleanup UPIs: Jo email hai ya jisme dot hai handle ke baad, use hatao
# #     upi_ids = []
# #     for upi in all_possible_upis:
# #         clean_upi = upi.strip().lower()
# #         # Agar isme dot hai @ ke baad (e.g. @bank.com), toh ye email hai
# #         handle_part = clean_upi.split('@')[-1]
# #         if '.' not in handle_part and clean_upi not in [e.lower() for e in emails]:
# #             upi_ids.append(upi)

# #     # 3. ---------- Phone Numbers (Space & Hyphen Safe) ----------
# #     phone_pattern = r"(?:\+91|91)?[\s\-]?\d{10}"
# #     phones = set(re.findall(phone_pattern, text))
# #     clean_phones = {re.sub(r"\D", "", p)[-10:] for p in phones}

# #     # 4. ---------- Bank Accounts ----------
# #     bank_pattern = r"\b\d{11,18}\b"
# #     raw_numbers = set(re.findall(bank_pattern, text))
# #     bank_context = ["acc", "account", "a/c", "bank", "transfer", "ifsc"]
    
# #     bank_accounts = []
# #     if any(ctx in text_lower for ctx in bank_context):
# #         for num in raw_numbers:
# #             if num[-10:] not in clean_phones:
# #                 bank_accounts.append(num)

# #     # ... baaki URLs aur Keywords (unme changes ki zarurat nahi)

# #     return {
# #         "upi_ids": list(set(upi_ids)), # Unique list
# #         "bank_accounts": list(set(bank_accounts)),
# #         "emails": list(emails),
# #         "phone_numbers": list(phones),
# #         "phishing_urls": list(set(re.findall(r"https?://\S+", text))),
# #         "suspicious_keywords": list({kw for kw in ["urgent", "suspended", "verify", "account"] if kw in text_lower}),
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
#             "suspicious_keywords": [],
#             "misc": {}
#         }

#     text_lower = text.lower()
    
#     # 1. ---------- Emails (Strict & Hyphen-Safe) ----------
#     # Ye bank-verify.com jaise hyphens aur dots ko pura capture karega
#     email_pattern = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
#     emails = set(re.findall(email_pattern, text))

#     # 2. ---------- UPI (Anti-Email & Dot-Safe Logic) ----------
#     # Pehle saare @ handles uthao
#     raw_upi_pattern = r"[\w\.-]+@[\w\.-]+"
#     potential_upis = re.findall(raw_upi_pattern, text)
    
#     upi_ids = []
#     for candidate in potential_upis:
#         candidate_lower = candidate.lower().strip()
        
#         # Split karke check karo ki @ ke baad wale part (handle) mein dot hai ya nahi
#         if "@" in candidate_lower:
#             parts = candidate_lower.split("@")
#             handle_part = parts[1] if len(parts) > 1 else ""
            
#             # CONDITION 1: UPI handle mein dot (.) nahi hota (jaise .com, .in)
#             # CONDITION 2: Wo kisi captured email ka hissa nahi hona chahiye
#             if "." not in handle_part:
#                 is_email_part = any(candidate_lower in e.lower() for e in emails)
#                 if not is_email_part:
#                     upi_ids.append(candidate)

#     # 3. ---------- Phone Numbers (Indian Context) ----------
#     # phone_pattern = r"(?:\+91|91)?[\s\-]?\d{10}"
#     # phones = set(re.findall(phone_pattern, text))
#     # # Comparison ke liye clean version (last 10 digits)
#     # clean_phones = {re.sub(r"\D", "", p)[-10:] for p in phones}
#     phone_pattern = r"(?:\+91|91)?[\s\-]?\b\d{10}\b" 
#     phones = set(re.findall(phone_pattern, text))
#     clean_phones = {re.sub(r"\D", "", p)[-10:] for p in phones}
#     # 4. ---------- Bank Accounts (Context Based) ----------
#     bank_pattern = r"\b\d{11,18}\b"
#     raw_bank_numbers = set(re.findall(bank_pattern, text))
#     final_phones = []
#     for p in phones:
#         clean_p = re.sub(r"\D", "", p)
#         # Agar ye phone kisi bade bank number ka hissa hai, toh ise hatao
#         if not any(clean_p in b for b in raw_bank_numbers):
#             final_phones.append(p)
#     bank_context_words = ["acc", "account", "a/c", "bank", "transfer", "ifsc", "beneficiary", "deposit"]
#     bank_accounts = []
    
#     if any(ctx in text_lower for ctx in bank_context_words):
#         for num in raw_numbers:
#             # Check: Phone number nahi hona chahiye (last 10 digits filter)
#             if num[-10:] not in clean_phones:
#                 bank_accounts.append(num)

#     # 5. ---------- Phishing URLs ----------
#     url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
#     urls = set(re.findall(url_pattern, text))

#     # 6. ---------- Suspicious Keywords ----------
#     suspicious_found = {kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower}

#     # Sab kuch list format mein return karo
#     return {
#         "upi_ids": list(set(upi_ids)),
#         "bank_accounts": list(set(bank_accounts)),
#         "phishing_urls": list(urls),
#         "phone_numbers": list(phones),
#         "emails": list(emails),
#         "suspicious_keywords": list(suspicious_found),
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
            "misc": {}
        }

    text_lower = text.lower()
    
    # 1 Emails
    email_pattern = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
    emails = set(re.findall(email_pattern, text))

    # 2.UPI 
    raw_upi_pattern = r"[\w\.-]+@[\w\.-]+"
    potential_upis = re.findall(raw_upi_pattern, text)
    
    upi_ids = []
    for candidate in potential_upis:
        candidate_lower = candidate.lower().strip()
        if "@" in candidate_lower:
            parts = candidate_lower.split("@")
            handle_part = parts[1] if len(parts) > 1 else ""
            
            if "." not in handle_part:
                if not any(candidate_lower in e.lower() for e in emails):
                    upi_ids.append(candidate)

    # 3.bank accounts
    bank_pattern = r"\b\d{11,18}\b"
    raw_bank_numbers = set(re.findall(bank_pattern, text))

    # 4. Phone Numbers 
    
    phone_pattern = r"(?:\+91|91)?[\s\-]?\b\d{10}\b" 
    found_phones = set(re.findall(phone_pattern, text))
    
    
    final_phones = []
    for p in found_phones:
        clean_p = re.sub(r"\D", "", p)[-10:]
        
        if not any(clean_p in b for b in raw_bank_numbers):
            final_phones.append(p)

    bank_context_words = ["acc", "account", "a/c", "bank", "transfer", "ifsc", "beneficiary", "deposit"]
    bank_accounts = []
    if any(ctx in text_lower for ctx in bank_context_words):
        bank_accounts = list(raw_bank_numbers)


    # order_pattern = r"(?:order\s*(?:id|number)?[:\-\s]+)([A-Za-z0-9\-]{5,})"
    # order_ids=set(re.findall(order_pattern,text, flags=re.IGNORECASE))

    # policy_pattern = r"(?:policy\s*{?:no|number)?[:\-\s]+)([A-Za-z0-9\-]{5,})"
    # policy_numbers= set(re.findall(policy_pattern, text, flags=re.IGNORECASE))

    # case_pattern = r"(?:case\s*(?:id|number)?[:\-\s]+)([A-Za-z0-9\-](5,})"
    # case_ids = set(re.findall(case_pattern, text, flags= re.IGNORECASE))
    # 5. url
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    urls = set(re.findall(url_pattern, text))

    order_ids = set()
    policy_numbers = set()
    case_ids = set()

    lines = text.splitlines()

    for line in lines:
        lower_line = line.lower()
        tokens = re.findall(r"\b[A-Za-z0-9\-]{4,}\b", line)

        for token in tokens:
            if token.isdigit() and len(token) < 4:
                continue

            if "order" in lower_line:
                order_ids.add(token)

            elif "policy" in lower_line:
                policy_numbers.add(token)

            elif "case" in lower_line:
                case_ids.add(token)

    # ---------------------------------------------------
    # 7. De-duplication Hierarchy
    # Priority: bank > order > policy > case
    # ---------------------------------------------------
    bank_set = set(bank_accounts)

    order_ids -= bank_set
    policy_numbers -= bank_set
    case_ids -= bank_set

    policy_numbers -= order_ids
    case_ids -= order_ids
    case_ids -= policy_numbers


    # 6. ---------- Suspicious Keywords ----------
    suspicious_found = {kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower}

    return {
        "upi_ids": list(upi_ids),
        "bank_accounts": list(bank_accounts),
        "phishing_urls": list(urls),
        "phone_numbers": list(set(final_phones)),
        "emails": list(emails),
        "order_ids": list(order_ids),
        "policy_numbers": list(policy_numbers),
        "case_ids": list(case_ids),
        "suspicious_keywords": list(suspicious_found),
        "misc": {}
    }
