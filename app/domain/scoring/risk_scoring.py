from decimal import Decimal
from typing import List, Dict
from collections import defaultdict

from app.domain.models.detection_result import DetectionResult
from app.domain.enums import RiskSeverity


class RiskScoringEngine:

    def __init__(
        self,
        medium_threshold: Decimal = Decimal("1000"),
        high_threshold: Decimal = Decimal("10000"),
    ):
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold

    def score(
        self,
        detections: List[DetectionResult],
        total_spend_by_currency: Dict[str, Decimal],
    ) -> Dict:

        vendor_totals = defaultdict(lambda: defaultdict(Decimal))
        currency_totals = defaultdict(Decimal)

        updated_detections = []

        for detection in detections:
            impact = detection.financial_impact_estimate
            currency = detection.currency

            severity = self._determine_severity(impact)

            detection = detection.model_copy(update={"risk_severity": severity})
            updated_detections.append(detection)

            vendor = detection.supporting_evidence.get("vendor", "unknown")

            vendor_totals[vendor][currency] += impact
            currency_totals[currency] += impact

        summary = self._build_summary(currency_totals, total_spend_by_currency)

        return {
            "updated_detections": updated_detections,
            "vendor_totals": dict(vendor_totals),
            "currency_totals": dict(currency_totals),
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

            percent_flagged = (
                (flagged_amount / total_spend) * 100
                if total_spend > 0
                else Decimal("0")
            )

            result[currency] = {
                "flagged_amount": flagged_amount,
                "total_spend": total_spend,
                "percent_flagged": percent_flagged,
            }

        return result
