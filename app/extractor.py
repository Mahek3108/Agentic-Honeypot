import re


def extract_intelligence(text: str):
    upi_pattern = r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b"
    bank_pattern = r"\b\d{9,18}\b"
    url_pattern = r"http[s]?://\S+"

    return {
        "upi_ids": re.findall(upi_pattern, text),
        "bank_accounts": re.findall(bank_pattern, text),
        "phishing_urls": re.findall(url_pattern, text)
    }
