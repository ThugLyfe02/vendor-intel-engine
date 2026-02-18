# Vendor Intelligence Engine

Deterministic financial anomaly detection engine for identifying vendor payment leakage with explainable risk scoring.

---

## 🔍 What It Detects

- Duplicate vendor payments
- Recurring subscription leakage
- Vendor-level risk concentration
- Currency-scoped financial impact

---

## 🧠 Design Philosophy

This engine prioritizes:

- Deterministic detection (no black-box ML)
- Financial precision (Decimal-safe calculations)
- Explainable rule triggers
- Enterprise-compatible architecture
- Modular detector framework
- Currency-aware aggregation
- Centralized risk normalization

---

## 🏗 Architecture Overview

Domain Layer  
- Transaction model (strict validation)  
- DetectionResult model (explainability contract)  
- BaseDetector interface  

Detection Layer  
- DuplicateDetector  
- RecurringDetector  

Scoring Layer  
- Centralized RiskScoringEngine  
- Vendor aggregation  
- Currency-level materiality  

Application Layer  
- VendorLeakEngine orchestrator  

Interface Layer  
- CLI entrypoint  

---

## 📂 Example Input

See: `examples/sample_transactions.csv`

---

## 📊 Example Output

See: `examples/sample_output.json`

The engine produces structured JSON containing:

- Detection results
- Financial impact estimates
- Vendor-level aggregation
- Currency totals
- Materiality summary

---

## 🚀 Planned Extensions

- Price drift detection
- Outlier anomaly detection
- Vendor alias normalization engine
- Configurable severity thresholds
- API wrapper (FastAPI)
- Containerized runtime
- Test coverage expansion

---

## ⚠️ Current Status

Core detection engine complete.  
Execution testing and Dockerization to follow.

---

## 📌 Why This Project Matters

Financial leakage in SMBs is often caused by:

- Duplicate payments
- Forgotten subscriptions
- Inconsistent vendor billing

This engine provides structured, explainable intelligence
instead of opaque AI predictions.

It is built to be auditable, deterministic, and extensible.

---

## 🔒 Risk & Audit Considerations

This engine is intentionally deterministic and explainable.

In financial environments, false positives and silent arithmetic errors create liability risk.

The system avoids:

- Floating point arithmetic
- Black-box ML scoring
- Implicit currency conversion
- Hidden state mutation

Design decisions prioritize auditability over complexity.
