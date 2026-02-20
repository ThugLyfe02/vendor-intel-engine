from decimal import Decimal
from typing import List, Dict
from collections import defaultdict

from app.domain.models.detection_result import DetectionResult
from app.domain.enums import RiskSeverity


class RiskScoringEngine:

    VERSION = "1.3.0"

    def __init__(
        self,
        medium_threshold: Decimal = Decimal("1000"),
        high_threshold: Decimal = Decimal("10000"),
        materiality_escalation_threshold: Decimal = Decimal("0.10"),  # 10%
    ):
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold
        self.materiality_escalation_threshold = materiality_escalation_threshold

    def score(
        self,
        detections: List[DetectionResult],
        total_spend_by_currency: Dict[str, Decimal],
    ) -> Dict:

        vendor_totals = defaultdict(lambda: defaultdict(Decimal))
        currency_totals = defaultdict(Decimal)
        updated_detections = []

        total_company_spend = sum(total_spend_by_currency.values())

        # First pass: apply base severity + aggregate vendor totals
        for detection in detections:

            impact = detection.financial_impact_estimate

            if impact <= Decimal("0"):
                continue

            currency = detection.currency

            base_severity = self._determine_severity(impact)

            normalized = detection.model_copy(
                update={"risk_severity": base_severity}
            )

            updated_detections.append(normalized)

            vendor = normalized.supporting_evidence.get("vendor", "unknown")

            vendor_totals[vendor][currency] += impact
            currency_totals[currency] += impact

        # Second pass: vendor-level materiality escalation
        if total_company_spend > Decimal("0"):
            for vendor, currency_map in vendor_totals.items():

                vendor_total_flagged = sum(currency_map.values())
                vendor_ratio = vendor_total_flagged / total_company_spend

                if vendor_ratio >= self.materiality_escalation_threshold:

                    for i, detection in enumerate(updated_detections):
                        if detection.supporting_evidence.get("vendor") == vendor:
                            updated_detections[i] = detection.model_copy(
                                update={"risk_severity": RiskSeverity.HIGH}
                            )

        # Deterministic ordering of aggregates
        sorted_vendor_totals = {
            vendor: dict(sorted(currency_map.items()))
            for vendor, currency_map in sorted(vendor_totals.items())
        }

        sorted_currency_totals = dict(sorted(currency_totals.items()))

        summary = self._build_summary(
            sorted_currency_totals,
            total_spend_by_currency,
        )

        return {
            "scoring_version": self.VERSION,
            "updated_detections": updated_detections,
            "vendor_totals": sorted_vendor_totals,
            "currency_totals": sorted_currency_totals,
            "summary": summary,
        }

    def _determine_severity(self, impact: Decimal) -> RiskSeverity:
        if impact >= self.high_threshold:
            return RiskSeverity.HIGH
        elif impact >= self.medium_threshold:
            return RiskSeverity.MEDIUM
        return RiskSeverity.LOW

    def _build_summary(
        self,
        flagged_totals: Dict[str, Decimal],
        total_spend_by_currency: Dict[str, Decimal],
    ) -> Dict:

        result = {}

        for currency, flagged_amount in flagged_totals.items():

            total_spend = total_spend_by_currency.get(currency, Decimal("0"))

            if total_spend > Decimal("0"):
                percent_flagged = (flagged_amount / total_spend) * Decimal("100")
            else:
                percent_flagged = Decimal("0")

            result[currency] = {
                "flagged_amount": flagged_amount,
                "total_spend": total_spend,
                "percent_flagged": percent_flagged,
            }

        return result
