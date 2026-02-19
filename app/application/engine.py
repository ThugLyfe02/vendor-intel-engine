def run(self, transactions: List[Transaction]) -> Dict:

    # Generate deterministic dataset fingerprint
    dataset_hash = generate_dataset_hash(transactions)

    all_detections = []

    # Run all detectors
    for detector in self.detectors:
        results = detector.detect(transactions)
        all_detections.extend(results)

    # Calculate total spend per currency
    total_spend_by_currency = self._calculate_total_spend(transactions)

    # Apply centralized scoring
    scored_results = self.scoring_engine.score(
        detections=all_detections,
        total_spend_by_currency=total_spend_by_currency,
    )

    # 🔐 Enforce deterministic output ordering
    sorted_detections = sorted(
        scored_results["updated_detections"],
        key=lambda d: (
            d.detection_type.value,
            d.currency,
            str(d.financial_impact_estimate),
            sorted(d.related_transaction_ids),
        )
    )

    return {
        "engine_version": ENGINE_VERSION,
        "dataset_hash": dataset_hash,
        "detections": sorted_detections,
        "vendor_totals": scored_results["vendor_totals"],
        "currency_totals": scored_results["currency_totals"],
        "summary": scored_results["summary"],
    }
