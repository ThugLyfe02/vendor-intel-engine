from datetime import timedelta
from decimal import Decimal
from typing import List
from collections import defaultdict

from app.domain.detection.base_detector import BaseDetector
from app.domain.models.transaction import Transaction
from app.domain.models.detection_result import DetectionResult
from app.domain.enums import DetectionType, RiskSeverity


class RecurringDetector(BaseDetector):

    VERSION = "1.0.1"

    def __init__(self, interval_tolerance_days: int = 3):
        self.interval_tolerance_days = interval_tolerance_days

    def detect(self, transactions: List[Transaction]) -> List[DetectionResult]:
        results: List[DetectionResult] = []

        grouped = defaultdict(list)

        # Group by vendor + currency + amount
        for tx in transactions:
            key = (tx.vendor_normalized_name, tx.currency, tx.amount)
            grouped[key].append(tx)

        for (vendor, currency, amount), tx_list in grouped.items():

            if len(tx_list) < 3:
                continue  # Require at least 3 occurrences to qualify as recurring

            tx_list.sort(key=lambda t: t.date)

            intervals = [
                (tx_list[i + 1].date - tx_list[i].date).days
                for i in range(len(tx_list) - 1)
            ]

            if self._is_consistent_interval(intervals):

                annualized_estimate = amount * Decimal("12")

                result = DetectionResult.create(
                    detection_type=DetectionType.RECURRING,
                    related_transaction_ids=[
                        t.transaction_id for t in tx_list
                    ],
                    rule_triggered="consistent_interval_recurring_pattern",
                    supporting_evidence={
                        "vendor": vendor,
                        "amount": str(amount),
                        "intervals_detected": intervals,
                        "detector_class": self.__class__.__name__,
                        "detector_version": self.VERSION,
                    },
                    financial_impact_estimate=annualized_estimate,
                    confidence_score=0.9,
                    risk_severity=self._determine_severity(annualized_estimate),
                    currency=currency,
                )

                results.append(result)

        return results

    def _is_consistent_interval(self, intervals: List[int]) -> bool:
        if not intervals:
            return False

        avg_interval = sum(intervals) / len(intervals)

        for interval in intervals:
            if abs(interval - avg_interval) > self.interval_tolerance_days:
                return False

        return True

    def _determine_severity(self, impact: Decimal) -> RiskSeverity:
        if impact >= Decimal("20000"):
            return RiskSeverity.HIGH
        elif impact >= Decimal("5000"):
            return RiskSeverity.MEDIUM
        return RiskSeverity.LOW
