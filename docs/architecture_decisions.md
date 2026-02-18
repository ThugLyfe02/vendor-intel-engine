# Architecture Decision Records

## ADR-001: Deterministic Detection Over ML

Decision:
Use deterministic rule-based detection instead of machine learning.

Rationale:
- Financial systems require explainability.
- Deterministic rules improve auditability.
- Reduces liability risk.
- Ensures reproducibility.

---

## ADR-002: Multi-Currency Support Without FX Conversion

Decision:
Support currency field from day one but avoid FX conversion logic.

Rationale:
- Enterprise compatibility.
- Avoid premature external API dependency.
- Prevent incorrect cross-currency aggregation.

---

## ADR-003: Centralized Risk Scoring Layer

Decision:
All detection results must pass through a centralized RiskScoringEngine.

Rationale:
- Prevent severity drift.
- Maintain consistent materiality thresholds.
- Enable future configurable scoring policies.
