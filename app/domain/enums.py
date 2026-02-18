from enum import Enum


class DetectionType(str, Enum):
    DUPLICATE = "duplicate"
    RECURRING = "recurring"
    PRICE_DRIFT = "price_drift"
    ANOMALY = "anomaly"


class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
