# PII Protocol — App Review Rating System

**Author:** Rohit
**Issue:** #<pii-issue-number>
**Phase:** 3 — Construction
**Status:** Active

---

## 1. Purpose

User-generated review text occasionally contains **Personally Identifiable Information (PII)** — emails, phone numbers, URLs, and social media handles. Training models on raw review text or persisting that text in logs creates real privacy and legal risk:

- PII becomes embedded in model weights, logs, and stored artifacts
- Sharing the dataset becomes legally sensitive under GDPR, CCPA, and similar regulations
- Future audits cannot easily prove that user data was handled responsibly

This protocol defines how PII is detected, masked, and audited across the pipeline.

---

## 2. Scope

### In scope
- `reviewText` field — masked via `src/pii_masker.py`
- Direct identifiers: emails, phone numbers, URLs, social handles

### Out of scope (handled elsewhere)
- `reviewerName` column — flagged for separate handling at the dataset-loading stage
- SSN, credit card, full home address — patterns prepared but not currently active; no observed occurrences in the dataset

### Intentionally not masked
- **Money references** (e.g. *"$20"*, *"10 dollars"*) — these correlate with refund discussions and carry meaningful sentiment signal for rating prediction. Masking them would damage downstream model performance.

---

## 3. PII Categories Handled

| Category | Replacement Token | Detection |
|---|---|---|
| Email addresses | `[EMAIL]` | Standard RFC-style regex |
| URLs | `[URL]` | Matches `http(s)://` and bare `www.` patterns |
| Phone numbers | `[PHONE]` | 10+ digit sequences with common separators |
| Social handles | `[HANDLE]` | `@username` (3–30 chars), excluding email contexts |
| Money amounts | *not masked* | Detected for observability only |

---

## 4. Quantitative Findings (from EDA)

Scan of all 111,143 reviews in `AppReviewData.csv`:

| Category | Reviews Affected | % of Dataset |
|---|---|---|
| Email | 3 | 0.003% |
| Phone | 8 | 0.007% |
| URL | 5 | 0.005% |
| Handle | 66 | 0.06% |
| Money (not masked) | 164 | 0.15% |

**Interpretation:** Direct PII occurs in fewer than 100 reviews (~0.08% of corpus). However, the masking infrastructure is established preventatively — at production scale (thousands of reviews per hour), even a 0.08% rate translates to dozens of PII-containing reviews daily.

---

## 5. Masking Strategy

### Replacement, not removal
PII is replaced with a bracketed placeholder token (e.g. `[EMAIL]`) rather than deleted. This preserves the structural information that "an email was here" — useful as a feature for the model — while removing the identifying value.

### Order of operations
Emails are masked **before** handles. Both patterns contain `@`, and reversing the order would corrupt email matches. The fixed order in `MASKING_ORDER` is:

1. `email`
2. `url`
3. `phone`
4. `handle`

### Irreversibility
Masking is **one-way**. The system does not retain a mapping from `[EMAIL]` back to the original email address. This is the safer default for ML training data and reduces audit surface.

---

## 6. Audit Trail

The `mask_pii(text, return_audit=True)` function returns a tuple of `(masked_text, audit_dict)` where `audit_dict` records every match per category. This supports:

- Per-record compliance reporting if required later
- Quality checks during pipeline development
- Verification that masking actually fired on records flagged as containing PII

The audit information is **not persisted** in the production dataset; it is available on demand from the masking function.

---

## 7. Limitations

1. **Obfuscated PII** — patterns like *"j.smith at gmail dot com"* or *"five five five one two three"* are not detected by regex. Catching these requires NLP-based entity recognition, which is out of scope for this prototype.
2. **Non-English formats** — phone numbers using non-Latin digits, or addresses in non-Latin scripts, are not currently scanned. The EDA found Hindi/Urdu content in the dataset, so this is a known gap.
3. **False negatives are accepted** — patterns are conservative. A small number of valid PII strings will pass through unmasked rather than risk corrupting legitimate review text.
4. **`reviewerName` column** — handled at the dataset level, not inside the text-masking module.

---

## 8. Roles and Ownership

| Concern | Owner |
|---|---|
| Maintain detection patterns | Lexicon / data quality lead |
| Apply masker in training pipeline | Modeling lead |
| Update protocol when new PII categories arise | Project lead |
| Review audit reports if produced | Project lead |

---

## 9. References

- Implementation: `src/pii_masker.py`
- Analysis notebook: `notebooks/pii_analysis.ipynb`
- EDA findings: `notebooks/Data_Exploration.ipynb`
