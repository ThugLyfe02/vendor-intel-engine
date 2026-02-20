from decimal import Decimal
from typing import Dict


class ExecutiveSummaryGenerator:

    VERSION = "1.0.0"

    def generate(self, engine_output: Dict) -> Dict:

        detections = engine_output.get("detections", [])
        vendor_ranking = engine_output.get("vendor_ranking", {}).get("ranked_vendors", {})
        summary = engine_output.get("summary", {})

        total_flagged = sum(
            d.get("financial_impact_estimate", Decimal("0"))
            for d in detections
        )

        total_annualized_exposure = self._compute_annualized_exposure(detections)

        top_vendors = list(vendor_ranking.keys())[:5]

        return {
            "summary_version": self.VERSION,
            "total_flagged_amount": total_flagged,
            "projected_12_month_exposure": total_annualized_exposure,
            "top_5_risk_vendors": top_vendors,
            "currency_summary": summary,
            "investigation_priority": self._generate_priority_list(vendor_ranking),
        }

    def _compute_annualized_exposure(self, detections):
        total = Decimal("0")

        for d in detections:
            if d.get("detection_type") == "recurring":
                total += Decimal(str(d.get("financial_impact_estimate", "0")))

        return total

    def _generate_priority_list(self, vendor_ranking):
        priority = []

        for vendor, data in list(vendor_ranking.items())[:5]:
            priority.append({
                "vendor": vendor,
                "risk_percentile": data.get("risk_percentile"),
                "flagged_spend": data.get("total_flagged_spend"),
            })

        return priority
