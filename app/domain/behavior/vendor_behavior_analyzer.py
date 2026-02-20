from decimal import Decimal, getcontext
from typing import List, Dict
from collections import defaultdict

from app.domain.models.transaction import Transaction


class VendorBehaviorAnalyzer:

    VERSION = "1.2.0"

    def analyze(self, transactions: List[Transaction]) -> Dict:

        vendor_groups = defaultdict(list)

        for tx in transactions:
            vendor_groups[tx.vendor_normalized_name].append(tx)

        vendor_profiles = {}

        for vendor, tx_list in vendor_groups.items():
            tx_list.sort(key=lambda t: t.date)

            amounts = [tx.amount for tx in tx_list]
            dates = [tx.date for tx in tx_list]

            interval_days = [
                (dates[i + 1] - dates[i]).days
                for i in range(len(dates) - 1)
            ]

            volatility_score = self._compute_decimal_volatility(amounts)
            interval_stability = self._compute_interval_stability(interval_days)
            duplicate_density = self._compute_duplicate_density(amounts)
            recurring_ratio = self._compute_recurring_ratio(interval_days)

            vendor_profiles[vendor] = {
                "behavior_version": self.VERSION,
                "transaction_count": len(tx_list),
                "amount_volatility_score": volatility_score,
                "interval_stability_score": interval_stability,
                "duplicate_density_rate": duplicate_density,
                "recurring_dependency_ratio": recurring_ratio,
            }

        return vendor_profiles

    def _compute_decimal_volatility(self, amounts: List[Decimal]) -> Decimal:
        if len(amounts) < 2:
            return Decimal("0")

        mean_val = sum(amounts) / Decimal(len(amounts))

        variance = sum(
            (a - mean_val) ** 2 for a in amounts
        ) / Decimal(len(amounts) - 1)

        return variance.sqrt()

    def _compute_interval_stability(self, intervals: List[int]) -> Decimal:
        if len(intervals) < 2:
            return Decimal("1")

        avg_interval = Decimal(sum(intervals)) / Decimal(len(intervals))

        variance = sum(
            (Decimal(i) - avg_interval) ** 2 for i in intervals
        ) / Decimal(len(intervals) - 1)

        return Decimal("1") / (Decimal("1") + variance)

    def _compute_duplicate_density(self, amounts: List[Decimal]) -> Decimal:
        if not amounts:
            return Decimal("0")

        unique_count = len(set(amounts))
        return Decimal("1") - (Decimal(unique_count) / Decimal(len(amounts)))

    def _compute_recurring_ratio(self, intervals: List[int]) -> Decimal:
        if not intervals:
            return Decimal("0")

        monthly_like = [i for i in intervals if abs(i - 30) <= 5]

        return Decimal(len(monthly_like)) / Decimal(len(intervals))
