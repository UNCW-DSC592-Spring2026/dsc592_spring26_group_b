"""
pii_masker.py
=============

Detects and masks Personally Identifiable Information (PII) in app review text.

Designed for use in the DSC592 App Review Rating prediction pipeline.
Replaces detected PII with bracketed placeholder tokens (e.g. [EMAIL], [PHONE])
so that downstream models retain structural information ("an email was here")
without storing the actual identifying values.

PII categories handled:
    - email      → [EMAIL]
    - url        → [URL]
    - phone      → [PHONE]
    - handle     → [HANDLE]   (e.g. @username)

The 'money' category (e.g. "$5", "10 dollars") is detected but intentionally
NOT masked — refund and price discussions carry sentiment signal that is
valuable for rating prediction.

Usage
-----
    from src.pii_masker import mask_pii

    masked = mask_pii("Email me at john@gmail.com")
    # 'Email me at [EMAIL]'

    masked, audit = mask_pii("Call 555-123-4567", return_audit=True)
    # 'Call [PHONE]', {'phone': ['555-123-4567'], ...}

Author: Rohit
Project: DSC592 — Software Engineering for Data Science
"""

import re


# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------
#
# Patterns are conservative — they prefer false negatives over false positives.
# Better to miss some PII than to mask legitimate text incorrectly.
#
PII_PATTERNS = {
    'email': re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    ),

    # Phone: requires 10+ digits (avoids matching version strings like 1.2.3)
    'phone': re.compile(
        r'(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
    ),

    # URL: matches http://, https://, or bare www.
    'url': re.compile(
        r'(?:https?://|www\.)[^\s,;]+',
        re.IGNORECASE
    ),

    # Handle: @username; negative lookbehind prevents matching inside emails
    'handle': re.compile(
        r'(?<![A-Za-z0-9])@[A-Za-z0-9_]{3,30}\b'
    ),

    # Money: detected for observability; NOT masked
    'money': re.compile(
        r'\$\s?\d+(?:[.,]\d+)?|\b\d+\s?(?:dollars?|usd|euros?|gbp|inr|rs)\b',
        re.IGNORECASE
    ),
}

# Order matters: emails must be masked before handles (both contain '@').
MASKING_ORDER = ['email', 'url', 'phone', 'handle']

REPLACEMENT_TOKENS = {
    'email':  '[EMAIL]',
    'url':    '[URL]',
    'phone':  '[PHONE]',
    'handle': '[HANDLE]',
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def mask_pii(text, return_audit=False):
    """
    Mask PII in a single piece of text.

    Parameters
    ----------
    text : str
        The review text to mask. Non-strings are coerced to strings.
        Null / NaN values return an empty string.
    return_audit : bool, default False
        If True, also return a dict of {category: [matched_strings]}
        documenting what was masked.

    Returns
    -------
    str
        The masked text.
    (str, dict)
        If return_audit is True.
    """
    if text is None or (isinstance(text, float) and text != text):  # NaN check
        return ("", {}) if return_audit else ""

    text = str(text)
    audit = {cat: [] for cat in PII_PATTERNS}

    for category in MASKING_ORDER:
        pattern = PII_PATTERNS[category]
        matches = pattern.findall(text)
        if matches:
            audit[category] = matches
            text = pattern.sub(REPLACEMENT_TOKENS[category], text)

    # 'money' is intentionally not masked — preserves sentiment signal
    money_matches = PII_PATTERNS['money'].findall(text)
    if money_matches:
        audit['money'] = money_matches  # observed, not masked

    if return_audit:
        return text, audit
    return text


def detect_pii(text):
    """
    Detect PII without masking. Returns counts per category.

    Parameters
    ----------
    text : str

    Returns
    -------
    dict[str, int]
        Counts of matches per PII category.
    """
    if text is None or (isinstance(text, float) and text != text):
        return {cat: 0 for cat in PII_PATTERNS}

    text = str(text)
    return {cat: len(pat.findall(text)) for cat, pat in PII_PATTERNS.items()}


# ---------------------------------------------------------------------------
# Demonstration / smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    samples = [
        "Email me at john.doe@gmail.com or call 555-123-4567.",
        "Visit www.example.com or https://app.io/help",
        "DM me @userhandle for help with my $20 refund",
        "This app is amazing, no complaints!",
        "Call (910) 555-1234 immediately!",
    ]

    print("=" * 70)
    print("PII MASKER — DEMONSTRATION")
    print("=" * 70)

    for s in samples:
        masked, audit = mask_pii(s, return_audit=True)
        found = {k: v for k, v in audit.items() if v}
        print(f"\nINPUT : {s}")
        print(f"OUTPUT: {masked}")
        if found:
            print(f"FOUND : {found}")
        else:
            print("FOUND : (no PII)")