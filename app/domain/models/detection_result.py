from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import List, Dict, Any
from uuid import uuid4

from app.domain.enums import DetectionType, RiskSeverity


class DetectionResult(BaseModel):
    detection_id: str
    detection_type: DetectionType
    related_transaction_ids: List[str]
    rule_triggered: str
    supporting_evidence: Dict[str, Any]
    financial_impact_estimate: Decimal
    confidence_score: float
    risk_severity: RiskSeverity
    currency: str

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("Confidence score must be between 0 and 1.")
        return v

    @classmethod
    def create(
        cls,
        detection_type: DetectionType,
        related_transaction_ids: List[str],
        rule_triggered: str,
        supporting_evidence: Dict[str, Any],
        financial_impact_estimate: Decimal,
        confidence_score: float,
        risk_severity: RiskSeverity,
        currency: str,
    ) -> "DetectionResult":
        return cls(
            detection_id=str(uuid4()),
            detection_type=detection_type,
            related_transaction_ids=related_transaction_ids,
            rule_triggered=rule_triggered,
            supporting_evidence=supporting_evidence,
            financial_impact_estimate=financial_impact_estimate,
            confidence_score=confidence_score,
            risk_severity=risk_severity,
            currency=currency,
        )
