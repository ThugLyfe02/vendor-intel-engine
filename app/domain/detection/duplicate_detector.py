from datetime import timedelta
from decimal import Decimal
from typing import List

from app.domain.detection.base_detector import BaseDetector
from app.domain.models.transaction import Transaction
from app.domain.models.detection_result import DetectionResult
from app.domain.enums import DetectionType, RiskSeverity


class DuplicateDetector(BaseDetector):

    def __init__(self, time_window_days: int = 7, min_amount: Decimal = Decimal("0.00")):
        self.time_window_days = time_window_days
        self.min_amount = min_amount

    def detect(self, transactions: List[Transaction]) -> List[DetectionResult]:
        results: List[DetectionResult] = []

        # Sort for deterministic processing
        transactions_sorted = sorted(
            transactions,
            key=lambda t: (t.vendor_normalized_name, t.currency, t.date)
        )

        for i in range(len(transactions_sorted)):
            current = transactions_sorted[i]

            if current.amount < self.min_amount:
                continue

            for j in range(i + 1, len(transactions_sorted)):
                candidate = transactions_sorted[j]

                # Stop when vendor changes (sorted by vendor)
                if candidate.vendor_normalized_name != current.vendor_normalized_name:
                    break

                # Currency must match
                if candidate.currency != current.currency:
                    continue

                # Amount must match exactly
                if candidate.amount != current.amount:
                    continue

                # Time window enforcement
                if candidate.date - current.date > timedelta(days=self.time_window_days):
                    break

                impact = current.amount

                result = DetectionResult.create(
                    detection_type=DetectionType.DUPLICATE,
                    related_transaction_ids=[current.transaction_id, candidate.transaction_id],
                    rule_triggered="same_vendor_same_amount_within_time_window",
                    supporting_evidence={
                        "vendor": current.vendor_normalized_name,
                        "amount": str(current.amount),
                        "time_window_days": self.time_window_days,
                    },
                    financial_impact_estimate=impact,
                    confidence_score=0.85,
                    risk_severity=self._determine_severity(impact),
                    currency=current.currency,
                )

                results.append(result)

        return results

    def _determine_severity(self, impact: Decimal) -> RiskSeverity:
        if impact >= Decimal("10000"):
            return RiskSeverity.HIGH
        elif impact >= Decimal("1000"):
            return RiskSeverity.MEDIUM
        return RiskSeverity.LOW
