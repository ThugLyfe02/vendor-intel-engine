# Test Specification

This document defines expected behavioral guarantees for the Vendor Intelligence Engine.

## 1. Duplicate Detection

Must:
- Detect same vendor + same amount within time window.
- Not detect across different currencies.
- Not detect outside time window.
- Remain deterministic across repeated runs.

Edge Cases:
- Installment payments.
- Refund offsets.
- Same-day multiple legitimate transactions.

---

## 2. Recurring Detection

Must:
- Require minimum 3 occurrences.
- Respect interval tolerance.
- Remain currency-scoped.
- Compute annualized estimate correctly.

Edge Cases:
- Seasonal billing.
- Irregular interval drift.
- Partial billing changes.

---

## 3. Risk Scoring

Must:
- Apply centralized thresholds.
- Preserve Decimal precision.
- Never mutate detection input.
- Produce consistent severity classification.

---

## 4. Dataset Fingerprinting

Must:
- Produce identical hash for identical datasets.
- Change hash if any transaction field changes.
- Remain order-independent.

---

## 5. Determinism Guarantee

Given identical dataset:
- Engine output must be identical.
- No stochastic behavior permitted.
