# Performance Considerations

The current implementation prioritizes determinism and clarity over premature optimization.

---

## Duplicate Detection Complexity

Current Approach:
- Vendor + currency grouping
- Time-window comparison within grouped transactions
- Worst-case complexity: O(n²) within vendor group

Rationale:
- Clarity and correctness first
- Deterministic evaluation
- Simpler reasoning during early-stage development

Future Optimization Options:
- Pre-index transactions by (vendor, currency, amount)
- Sliding time-window strategy
- Hash-map grouping to reduce nested iteration
- Early break logic refinement
- Batch processing for large datasets

---

## Recurring Detection Complexity

Current Approach:
- Grouping by vendor + currency + amount
- Interval consistency validation

Future Improvements:
- Interval histogram analysis
- Efficient rolling interval tracking
- Sparse pattern detection for long time-series

---

## Dataset Fingerprinting

Hashing complexity is O(n) and scales linearly with dataset size.

Future enhancement:
- Parallelized hashing for large-scale ingestion
- Stream-based fingerprinting

---

## Scaling Philosophy

The engine is designed to:

- Optimize for deterministic correctness first
- Harden behavior before optimizing performance
- Introduce optimization only after profiling real workloads

Premature optimization is intentionally avoided.
