from decimal import Decimal
from typing import List, Dict

from app.domain.models.transaction import Transaction
from app.domain.models.detection_result import DetectionResult
from app.domain.detection.duplicate_detector import DuplicateDetector
from app.domain.detection.recurring_detector import RecurringDetector


class VendorLeakEngine:

    def __init__(self):
        self.detectors = [
            DuplicateDetector(),
            RecurringDetector(),
        ]

    def run(self, transactions: List[Transaction]) -> Dict:
        all_detections: List[DetectionResult] = []

        for detector in self.detectors:
            results = detector.detect(transactions)
            all_detections.extend(results)

        total_spend_by_currency = self._calculate_total_spend(transactions)

        return {
            "detections": all_detections,
            "total_spend_by_currency": total_spend_by_currency,
        }

    def _calculate_total_spend(self, transactions: List[Transaction]) -> Dict[str, Decimal]:
        totals: Dict[str, Decimal] = {}

        for tx in transactions:
            totals.setdefault(tx.currency, Decimal("0"))
            totals[tx.currency] += tx.amount

        return totals
