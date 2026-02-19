from decimal import Decimal
from typing import List, Dict

from app.domain.models.transaction import Transaction
from app.domain.detection.duplicate_detector import DuplicateDetector
from app.domain.detection.recurring_detector import RecurringDetector
from app.domain.scoring.risk_scoring import RiskScoringEngine
from app.domain.utils.dataset_fingerprint import generate_dataset_hash


ENGINE_VERSION = "0.1.0"


class VendorLeakEngine:

    def __init__(self):
        self.detectors = [
            DuplicateDetector(),
            RecurringDetector(),
        ]
        self.scoring_engine = RiskScoringEngine()

    def run(self, transactions: List[Transaction]) -> Dict:

        dataset_hash = generate_dataset_hash(transactions)

        all_detections = []

        for detector in self.detectors:
            results = detector.detect(transactions)
            all_detections.extend(results)

        total_spend_by_currency = self._calculate_total_spend(transactions)

        scored_results = self.scoring_engine.score(
            detections=all_detections,
            total_spend_by_currency=total_spend_by_currency,
        )

        return {
            "engine_version": ENGINE_VERSION,
            "dataset_hash": dataset_hash,
            "detections": scored_results["updated_detections"],
            "vendor_totals": scored_results["vendor_totals"],
            "currency_totals": scored_results["currency_totals"],
            "summary": scored_results["summary"],
        }

    def _calculate_total_spend(self, transactions: List[Transaction]) -> Dict[str, Decimal]:
        totals: Dict[str, Decimal] = {}

        for tx in transactions:
            totals.setdefault(tx.currency, Decimal("0"))
            totals[tx.currency] += tx.amount

        return totals
