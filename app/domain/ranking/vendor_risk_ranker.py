from decimal import Decimal
from typing import Dict


class VendorRiskRanker:

    VERSION = "1.3.0"

    def rank(
        self,
        vendor_totals: Dict,
        vendor_behavior_profiles: Dict,
        total_spend_by_currency: Dict[str, Decimal],
    ) -> Dict:

        total_company_spend = sum(total_spend_by_currency.values())

        vendor_scores = {}

        # First pass: compute raw composite risk scores
        for vendor in sorted(vendor_totals.keys()):

            currency_map = vendor_totals[vendor]
            total_flagged_spend = sum(currency_map.values())

            if total_company_spend == Decimal("0"):
                continue

            flagged_ratio = total_flagged_spend / total_company_spend

            behavior = vendor_behavior_profiles.get(vendor, {})

            volatility = behavior.get("amount_volatility_score", Decimal("0"))
            duplicate_density = behavior.get("duplicate_density_rate", Decimal("0"))
            recurring_ratio = behavior.get("recurring_dependency_ratio", Decimal("0"))

            # Composite deterministic score
            raw_score = (
                float(flagged_ratio) * 4
                + float(volatility) * 0.5
                + float(duplicate_density) * 2
                + float(recurring_ratio) * 2
            )

            vendor_scores[vendor] = {
                "raw_score": raw_score,
                "total_flagged_spend": total_flagged_spend,
                "flagged_ratio": flagged_ratio,
            }

        # Normalize scores to 0–1 range
        raw_values = [data["raw_score"] for data in vendor_scores.values()]

        if not raw_values:
            return {
                "ranking_version": self.VERSION,
                "ranked_vendors": {},
            }

        min_score = min(raw_values)
        max_score = max(raw_values)

        normalized_scores = {}

        for vendor, data in vendor_scores.items():

            if max_score > min_score:
                normalized = (data["raw_score"] - min_score) / (max_score - min_score)
            else:
                normalized = 1.0

            normalized_scores[vendor] = {
                "normalized_risk_score": normalized,
                "total_flagged_spend": data["total_flagged_spend"],
                "flagged_ratio": data["flagged_ratio"],
            }

        # Deterministic descending ranking
        sorted_vendors = sorted(
            normalized_scores.items(),
            key=lambda item: item[1]["normalized_risk_score"],
            reverse=True,
        )

        total_vendors = len(sorted_vendors)

        ranked = {}

        for idx, (vendor, data) in enumerate(sorted_vendors):

            if total_vendors > 1:
                percentile = 1 - (idx / (total_vendors - 1))
            else:
                percentile = 1.0

            ranked[vendor] = {
                **data,
                "risk_percentile": percentile,
            }

        return {
            "ranking_version": self.VERSION,
            "ranked_vendors": ranked,
        }
