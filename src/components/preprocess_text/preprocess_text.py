import argparse
import os
import re

import nltk
import pandas as pd

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# ---------------------------------------------------------------------------
# PII Masking Patterns and Functions
# ---------------------------------------------------------------------------
#
# Detects and masks Personally Identifiable Information (PII) in app review text.
# Replaces detected PII with bracketed placeholder tokens (e.g. [EMAIL], [PHONE])
#
# PII categories handled:
#     - email      → [EMAIL]
#     - url        → [URL]
#     - phone      → [PHONE]
#     - handle     → [HANDLE]   (e.g. @username)
#
# The 'money' category is detected but intentionally NOT masked — refund and
# price discussions carry sentiment signal that is valuable for rating prediction.
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
# Text Preprocessing
# ---------------------------------------------------------------------------

def preprocess(text: str, args) -> str:
    # Step 1: Mask PII early in the pipeline (before other transformations)
    if args.mask_pii:
        text = mask_pii(text)

    if args.normalize_case:
        text = text.lower()
    if args.remove_urls:
        text = re.sub(r'http\S+|www\.\S+', '', text)
    if args.remove_emails:
        text = re.sub(r'\S+@\S+', '', text)
    if args.remove_numbers:
        text = re.sub(r'\d+', '', text)
    if args.normalize_backslashes:
        text = text.replace('\\', '/')
    if args.split_on_special_chars:
        text = re.sub(r'[_\-/]', ' ', text)
    if args.remove_special_chars:
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    if args.remove_duplicate_chars:
        text = re.sub(r'(.)\1{2,}', r'\1', text)

    tokens = word_tokenize(text)

    if args.remove_stop_words:
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t.lower() not in stop_words]

    if args.use_lemmatization:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return ' '.join(tokens)


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess review text with optional PII masking."
    )
    parser.add_argument('--dataset', required=True, help='Input dataset directory')
    parser.add_argument('--text_column', default='reviewText', help='Name of text column')
    parser.add_argument('--results_dataset', required=True, help='Output dataset directory')

    # PII masking
    parser.add_argument(
        '--mask_pii',
        type=lambda x: x.lower() == 'true',
        default=True,
        help='Mask PII (email, phone, URL, handle) before other preprocessing'
    )

    # Text normalization
    parser.add_argument(
        '--remove_stop_words',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--use_lemmatization',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--normalize_case',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--remove_numbers',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--remove_special_chars',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--remove_duplicate_chars',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--remove_emails',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--remove_urls',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--normalize_backslashes',
        type=lambda x: x.lower() == 'true',
        default=True
    )
    parser.add_argument(
        '--split_on_special_chars',
        type=lambda x: x.lower() == 'true',
        default=True
    )

    args = parser.parse_args()

    # Load dataset
    csv_files = [f for f in os.listdir(args.dataset) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(args.dataset, csv_files[0]))

    # Preprocess text column
    df[args.text_column] = (
        df[args.text_column]
        .fillna('')
        .astype(str)
        .apply(lambda t: preprocess(t, args))
    )

    # Save results
    os.makedirs(args.results_dataset, exist_ok=True)
    df.to_csv(os.path.join(args.results_dataset, 'output.csv'), index=False)
    print(f"Preprocessed {len(df)} rows → {args.results_dataset}")


if __name__ == '__main__':
    main()
