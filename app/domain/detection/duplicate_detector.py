from datetime import timedelta
from decimal import Decimal
from typing import List
from collections import defaultdict

from app.domain.detection.base_detector import BaseDetector
from app.domain.models.transaction import Transaction
from app.domain.models.detection_result import DetectionResult
from app.domain.enums import DetectionType, RiskSeverity


class DuplicateDetector(BaseDetector):

    VERSION = "1.4.0"

    def __init__(self, time_window_days: int = 7, min_amount: Decimal = Decimal("0.00")):
        self.time_window_days = time_window_days
        self.min_amount = min_amount

    def detect(self, transactions: List[Transaction]) -> List[DetectionResult]:

        results: List[DetectionResult] = []

        # Primary grouping by vendor + currency
        vendor_currency_groups = defaultdict(list)

        for tx in transactions:
            if tx.amount < self.min_amount:
                continue
            key = (tx.vendor_normalized_name, tx.currency)
            vendor_currency_groups[key].append(tx)

        for (vendor, currency), tx_list in vendor_currency_groups.items():

            # Secondary grouping by amount
            amount_groups = defaultdict(list)

            for tx in tx_list:
                amount_groups[tx.amount].append(tx)

            for amount, amount_list in amount_groups.items():

                if len(amount_list) < 2:
                    continue

                amount_list.sort(key=lambda t: t.date)

                # 🔒 Installment suppression logic
                if self._is_structured_installment(amount_list):
                    continue

                window_start = 0

                for window_end in range(1, len(amount_list)):

                    while (
                        amount_list[window_end].date - amount_list[window_start].date
                        > timedelta(days=self.time_window_days)
                    ):
                        window_start += 1

                    if window_start != window_end:
                        current = amount_list[window_start]
                        candidate = amount_list[window_end]

                        result = DetectionResult.create(
                            detection_type=DetectionType.DUPLICATE,
                            related_transaction_ids=[
                                current.transaction_id,
                                candidate.transaction_id,
                            ],
                            rule_triggered="indexed_vendor_currency_amount_window",
                            supporting_evidence={
                                "vendor": vendor,
                                "amount": str(amount),
                                "time_window_days": self.time_window_days,
                                "installment_suppressed": False,
                                "detector_class": self.__class__.__name__,
                                "detector_version": self.VERSION,
                            },
                            financial_impact_estimate=amount,
                            confidence_score=0.85,
                            risk_severity=self._determine_severity(amount),
                            currency=currency,
                        )

                        results.append(result)

        return results

    def _is_structured_installment(self, tx_list: List[Transaction]) -> bool:
        """
        Detect structured installment payments to avoid false duplicate flags.

        Criteria:
        - Minimum 3 occurrences
        - Consistent interval pattern
        - Stable amount (already grouped)
        """

        if len(tx_list) < 3:
            return False

        intervals = [
            (tx_list[i + 1].date - tx_list[i].date).days
            for i in range(len(tx_list) - 1)
        ]

        if not intervals:
            return False

        avg_interval = sum(intervals) / len(intervals)
        tolerance = 5  # Days tolerance

        consistent_pattern = all(
            abs(i - avg_interval) <= tolerance for i in intervals
        )

        return consistent_pattern

    def _determine_severity(self, impact: Decimal) -> RiskSeverity:
        if impact >= Decimal("10000"):
            return RiskSeverity.HIGH
        elif impact >= Decimal("1000"):
            return RiskSeverity.MEDIUM
        return RiskSeverity.LOW
