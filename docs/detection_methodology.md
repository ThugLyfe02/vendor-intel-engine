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
