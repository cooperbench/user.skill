"""Per-entity heuristics adapted from SWE-chat-private redact_PII.py."""
from __future__ import annotations

import string


def not_valid_url(s: str, context_local: str, full_msg: str) -> bool:
    # Keep nearly every URL — only redact sensitive social-profile URLs.
    if "linkedin.com/in/" in s:
        return False
    return True


def not_valid_card(s: str, context_local: str, full_msg: str) -> bool:
    if "card" not in context_local.lower():
        return True
    return False


def not_valid_email(s: str, context_local: str, full_msg: str) -> bool:
    lo = s.lower()
    placeholder_domains = (
        "@example.com",
        "@domain.com",
        "@email.com",
        "@login.com",
        "@xxxxx.com",
        "@xxxx.com",
        "@xxx.com",
        "@xx.com",
        "@x.com",
        "@companyname.com",
    )
    if any(dom in lo for dom in placeholder_domains):
        return True
    generic_prefixes = (
        "webmaster@",
        "login@",
        "abcdefg@",
        "info@",
        "feedback@",
        "partners@",
        "events@",
        "orders@",
        "shipping@",
        "quality@",
        "reservations@",
        "inquiries@",
        "complaints@",
        "contact@",
        "computer@",
        "test@",
        "email@",
    )
    if any(lo.startswith(p) or p in lo for p in generic_prefixes):
        return True
    if lo.startswith("your@"):
        return True
    if "/" in s:
        return True
    if '"email":' in context_local.lower():
        return True
    return False


def not_valid_phone(s: str, context_local: str, full_msg: str) -> bool:
    if len(s) <= 8:
        return True
    if "  " in s:
        return True
    for private_ip_prefix in ("192.168.", "127.0.", "255.255."):
        if private_ip_prefix in s:
            return True
    allowed = set("0123456789-() +")
    if any(c not in allowed for c in s):
        return True
    required = (
        " m:",
        "\nm:",
        "tel.",
        "tel:",
        "tel ",
        "phone",
        "whatsapp",
        "wechat",
    )
    ok = False
    lo = context_local.lower()
    for r in required:
        if r in lo:
            ok = True
    if (
        s.startswith("+")
        and len(s) > 1
        and s[1].isdigit()
        and context_local
        and context_local[-1] in " \n\t"
    ):
        ok = True
    return not ok


def not_valid_person(s: str, context_local: str, full_msg: str) -> bool:
    if "\n" in s:
        return True
    if any(c.isdigit() for c in s):
        return True
    if " the " in s:
        return True
    if s.strip() != s:
        return True
    if len(s) <= 1:
        return True
    bad_punc = set(string.punctuation) - {".", "-"}
    if any(p in s for p in bad_punc):
        return True
    if s.endswith(".") or s.endswith("-") or s.startswith(".") or s.startswith("-"):
        return True
    if "- " in s or " -" in s:
        return True
    if len(s.split()) < 2:
        return True
    if s[0].islower():
        return True
    hooks = (
        "my name is ",
        "i am ",
        "i'm ",
        "this is ",
        "best,",
        "best regard",
        "best wish",
        "sincerely,",
        "regards",
        "thanks,",
        "thanks ",
        "yours ",
        "yours,",
        "faithfully,",
        "cheers,",
        "take care,",
        "dear ",
        "hello ",
        "hi ",
    )
    lo = context_local.lower()
    if not any(h in lo for h in hooks):
        return True
    return False


VALIDATORS = {
    "PERSON": not_valid_person,
    "PHONE_NUMBER": not_valid_phone,
    "EMAIL_ADDRESS": not_valid_email,
    "CREDIT_CARD": not_valid_card,
    "URL": not_valid_url,
}

# Document-frequency thresholds (Joe defaults). Used when freqs are provided.
THRESHOLDS = {
    "PERSON": 50,
    "PHONE_NUMBER": 10,
    "EMAIL_ADDRESS": 10,
    "CREDIT_CARD": 10,
    "URL": 500,
}

REDACT_ENTITIES = [
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "EMAIL_ADDRESS",
    "PERSON",
    "URL",
]

# Broader set for detection (Joe's run_presidio_ner ENTITIES).
DETECT_ENTITIES = [
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "CRYPTO",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "IP_ADDRESS",
    "PERSON",
    "MEDICAL_LICENSE",
    "US_BANK_NUMBER",
    "US_DRIVER_LICENSE",
    "US_PASSPORT",
    "US_SSN",
    "US_ITIN",
    "UK_NHS",
    "NRP",
    "LOCATION",
    "DATE_TIME",
    "URL",
]
