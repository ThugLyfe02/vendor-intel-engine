from decimal import Decimal
from typing import List, Dict

from app.domain.models.transaction import Transaction
from app.domain.detection.duplicate_detector import DuplicateDetector
from app.domain.detection.recurring_detector import RecurringDetector
from app.domain.scoring.risk_scoring import RiskScoringEngine
from app.domain.utils.dataset_fingerprint import generate_dataset_hash
from app.domain.behavior.vendor_behavior_analyzer import VendorBehaviorAnalyzer


ENGINE_VERSION = "0.2.0"


class VendorLeakEngine:

    def __init__(self):
        self.detectors = [
            DuplicateDetector(),
            RecurringDetector(),
        ]
        self.scoring_engine = RiskScoringEngine()
        self.behavior_analyzer = VendorBehaviorAnalyzer()

    def run(self, transactions: List[Transaction]) -> Dict:

        # Deterministic dataset fingerprint
        dataset_hash = generate_dataset_hash(transactions)

        all_detections = []

        # Run detection modules
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

        # Deterministic detection ordering
        sorted_detections = sorted(
            scored_results["updated_detections"],
            key=lambda d: (
                d.detection_type.value,
                d.currency,
                str(d.financial_impact_estimate),
                sorted(d.related_transaction_ids),
            )
        )

        # Compute vendor behavioral fingerprints
        vendor_behavior_profiles = self.behavior_analyzer.analyze(transactions)

        return {
            "engine_version": ENGINE_VERSION,
            "dataset_hash": dataset_hash,
            "detections": sorted_detections,
            "vendor_totals": scored_results["vendor_totals"],
            "currency_totals": scored_results["currency_totals"],
            "summary": scored_results["summary"],
            "vendor_behavior_profiles": vendor_behavior_profiles,
        }

    def _calculate_total_spend(self, transactions: List[Transaction]) -> Dict[str, Decimal]:
        totals: Dict[str, Decimal] = {}

        for tx in transactions:
            totals.setdefault(tx.currency, Decimal("0"))
            totals[tx.currency] += tx.amount

        return totals
