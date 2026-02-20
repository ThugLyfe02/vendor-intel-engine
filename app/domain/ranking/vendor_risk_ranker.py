from decimal import Decimal
from typing import Dict


class VendorRiskRanker:

    VERSION = "1.0.0"

    def rank(
        self,
        vendor_totals: Dict,
        vendor_behavior_profiles: Dict,
        total_spend_by_currency: Dict[str, Decimal],
    ) -> Dict:

        vendor_scores = {}

        for vendor, currency_map in vendor_totals.items():

            total_flagged_spend = sum(currency_map.values())

            total_company_spend = sum(total_spend_by_currency.values())

            if total_company_spend == Decimal("0"):
                continue

            flagged_ratio = total_flagged_spend / total_company_spend

            behavior = vendor_behavior_profiles.get(vendor, {})

            volatility = behavior.get("amount_volatility_score", 0)
            duplicate_density = behavior.get("duplicate_density_rate", 0)
            recurring_ratio = behavior.get("recurring_dependency_ratio", 0)

            # Composite deterministic risk score
            risk_score = (
                float(flagged_ratio) * 4
                + float(volatility) * 0.5
                + float(duplicate_density) * 2
                + float(recurring_ratio) * 2
            )

            vendor_scores[vendor] = {
                "risk_score": risk_score,
                "total_flagged_spend": total_flagged_spend,
                "flagged_ratio": flagged_ratio,
                "volatility": volatility,
                "duplicate_density": duplicate_density,
                "recurring_ratio": recurring_ratio,
            }

        # Deterministic descending ranking
        ranked = dict(
            sorted(
                vendor_scores.items(),
                key=lambda item: item[1]["risk_score"],
                reverse=True,
            )
        )

        return {
            "ranking_version": self.VERSION,
            "ranked_vendors": ranked,
        }
