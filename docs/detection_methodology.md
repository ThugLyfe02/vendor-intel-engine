# Detection Methodology

## Duplicate Detection

Rule:
- Same normalized vendor
- Same currency
- Same amount
- Within configurable time window

Risk:
May falsely detect installment payments.

Mitigation:
Future addition of invoice reference matching.

---

## Recurring Detection

Rule:
- Same vendor
- Same amount
- At least 3 occurrences
- Consistent interval within tolerance

Risk:
Seasonal billing may appear recurring.

Mitigation:
Future contract metadata integration.

---

## Risk Scoring

Severity determined by:
- Absolute financial impact
- Configurable thresholds

Future:
Materiality relative to total spend.

--- 

---

### Installment Protection (Planned Enhancement)

Risk:
Structured installment payments (e.g., split invoices, scheduled financing) may be incorrectly flagged as duplicates.

Planned Mitigation:

- Compare invoice references when available.
- Detect consistent installment schedules (equal amounts at predefined intervals).
- Suppress duplicate flags when installment patterns are confirmed.
- Introduce installment classification layer prior to duplicate evaluation.

Rationale:

Duplicate detection must distinguish between:

- Accidental duplicate payments  
- Intentional installment structures  

This enhancement preserves detection precision while reducing false positives in structured billing scenarios.
