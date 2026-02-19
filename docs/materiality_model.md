# Materiality Model

The Materiality Model determines the significance of detected financial leakage relative to business size.

## Objective

Move from:
- Absolute dollar thresholds

To:
- Context-aware financial impact evaluation

---

## Core Principle

A $2,000 anomaly is not equally material in:

- A $200,000 company
- A $50,000,000 company

Materiality must scale relative to total spend.

---

## Proposed Materiality Score (Conceptual)

Materiality Score =
    (Flagged Amount / Total Company Spend)
    × 100

Vendor Materiality Score =
    (Flagged Vendor Spend / Total Vendor Spend)
    × 100

---

## Risk Calibration Layer

Severity tiers should consider:

- Absolute amount
- Relative materiality
- Confidence score
- Recurrence frequency

Example:

High Severity:
- High absolute amount
- OR high materiality percentage
- AND high confidence

---

## Why This Matters

Traditional accounting tools use static thresholds.

Enterprise-grade systems use relative financial exposure modeling.

This engine is designed to support:

- Context-aware risk evaluation
- Proportional severity calibration
- Executive decision-level insights
