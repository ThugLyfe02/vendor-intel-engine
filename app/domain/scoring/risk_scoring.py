from decimal import Decimal
from typing import List, Dict
from collections import defaultdict

from app.domain.models.detection_result import DetectionResult
from app.domain.enums import RiskSeverity


class RiskScoringEngine:
    """
    Centralized deterministic risk normalization engine.

    Responsibilities:
    - Enforce non-zero financial impact floor
    - Apply centralized severity thresholds
    - Aggregate vendor-level totals
    - Aggregate currency-level totals
    - Compute materiality summary
    """

    VERSION = "1.1.0"

    def __init__(
        self,
        medium_threshold: Decimal = Decimal("1000"),
        high_threshold: Decimal = Decimal("10000"),
        minimum_materiality_floor: Decimal = Decimal("0.01"),
    ):
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold
        self.minimum_materiality_floor = minimum_materiality_floor

    def score(
        self,
        detections: List[DetectionResult],
        total_spend_by_currency: Dict[str, Decimal],
    ) -> Dict:

        vendor_totals: Dict[str, Dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
        currency_totals: Dict[str, Decimal] = defaultdict(Decimal)

        updated_detections: List[DetectionResult] = []

        for detection in detections:

            impact = detection.financial_impact_estimate

            # 🔐 Strict financial floor enforcement
            if (
                impact is None
                or impact <= Decimal("0")
                or impact < self.minimum_materiality_floor
            ):
                continue

            currency = detection.currency

            # Deterministic severity normalization
            severity = self._determine_severity(impact)

            # Create immutable updated detection
            normalized_detection = detection.model_copy(
                update={
                    "risk_severity": severity
                }
            )

            updated_detections.append(normalized_detection)

            vendor = normalized_detection.supporting_evidence.get("vendor", "unknown")

            vendor_totals[vendor][currency] += impact
            currency_totals[currency] += impact

        # Deterministic ordering of vendor totals
        sorted_vendor_totals = {
            vendor: dict(sorted(currency_map.items()))
            for vendor, currency_map in sorted(vendor_totals.items())
        }

        sorted_currency_totals = dict(sorted(currency_totals.items()))

        summary = self._build_summary(
            sorted_currency_totals,
            total_spend_by_currency
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
                percent_flagged = (
                    flagged_amount / total_spend
                ) * Decimal("100")
            else:
                percent_flagged = Decimal("0")

            result[currency] = {
                "flagged_amount": flagged_amount,
                "total_spend": total_spend,
                "percent_flagged": percent_flagged,
            }

        return result
