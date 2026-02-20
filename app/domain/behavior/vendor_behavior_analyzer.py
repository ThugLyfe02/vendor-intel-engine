from decimal import Decimal
from typing import List, Dict
from collections import defaultdict
from statistics import mean, stdev
from datetime import timedelta

from app.domain.models.transaction import Transaction


class VendorBehaviorAnalyzer:

    VERSION = "1.0.0"

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

            volatility_score = self._compute_volatility(amounts)
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

    def _compute_volatility(self, amounts: List[Decimal]) -> float:
        if len(amounts) < 2:
            return 0.0
        numeric_amounts = [float(a) for a in amounts]
        return stdev(numeric_amounts)

    def _compute_interval_stability(self, intervals: List[int]) -> float:
        if len(intervals) < 2:
            return 1.0
        return 1.0 / (1.0 + stdev(intervals))

    def _compute_duplicate_density(self, amounts: List[Decimal]) -> float:
        if not amounts:
            return 0.0
        unique_count = len(set(amounts))
        return 1.0 - (unique_count / len(amounts))

    def _compute_recurring_ratio(self, intervals: List[int]) -> float:
        if not intervals:
            return 0.0
        avg_interval = mean(intervals)
        monthly_like = [i for i in intervals if abs(i - 30) <= 5]
        return len(monthly_like) / len(intervals)
