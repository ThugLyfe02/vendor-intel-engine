# Policy Framework

The Policy Framework introduces configurable financial risk rules that govern detection behavior and severity calibration.

## Objective

Move from:
- Hardcoded thresholds

To:
- Configurable, policy-driven risk governance

---

## Policy Types

### 1. Detection Policy

Defines:

- Duplicate time window (days)
- Recurring interval tolerance
- Minimum materiality threshold
- Minimum confidence threshold

Example:

DuplicatePolicy:
  time_window_days: 7
  min_amount_threshold: 100

RecurringPolicy:
  interval_tolerance_days: 3
  min_occurrences: 3

---

### 2. Severity Calibration Policy

Defines:

- Medium severity threshold
- High severity threshold
- Relative materiality override

Example:

SeverityPolicy:
  medium_threshold: 1000
  high_threshold: 10000
  materiality_override_percentage: 5%

---

### 3. Vendor Risk Policy

Defines:

- Vendor risk concentration threshold
- Recurring exposure multiplier
- Duplicate frequency escalation rules

---

## Why This Matters

Most accounting tools operate with static logic.

Enterprise systems operate with:

Policy-driven governance layers.

This enables:

- Industry-specific tuning
- Business-size customization
- Compliance alignment
- Future SaaS configuration layers

---

## Future Evolution

The Policy Framework can evolve into:

- JSON-configurable policies
- Database-backed policy storage
- Multi-tenant SaaS configuration
- Role-based policy enforcement
