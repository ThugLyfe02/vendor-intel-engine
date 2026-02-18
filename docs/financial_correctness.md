# Financial Correctness Guarantees

This engine is designed with financial integrity as a core constraint.

## 1. Decimal-Safe Calculations

All monetary values use Python's `Decimal` type to prevent floating-point drift.

No float-based arithmetic is used for financial impact estimation.

---

## 2. Deterministic Detection

Detection logic is rule-based and reproducible.

Given identical input data, output will always be identical.

No probabilistic behavior is introduced in core detection modules.

---

## 3. Currency Isolation

All aggregation and impact estimation is performed within currency boundaries.

No cross-currency aggregation is performed without explicit FX handling.

---

## 4. Explicit Severity Calibration

Risk severity is determined using configurable materiality thresholds.

Severity classification is not arbitrary and is centralized.

---

## 5. No Silent Mutation

Transactions are never mutated during detection.

All detection modules are read-only.

---

## 6. Explainability by Design

Every detection result includes:

- Rule triggered
- Supporting evidence
- Financial impact estimate
- Confidence score
- Risk severity

This ensures audit traceability.
