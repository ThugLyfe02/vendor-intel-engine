from decimal import Decimal


class EngineConfig:

    VERSION = "1.0.0"

    # Duplicate detection
    DUPLICATE_TIME_WINDOW_DAYS = 7
    DUPLICATE_MIN_AMOUNT = Decimal("0.00")

    # Severity thresholds
    MEDIUM_THRESHOLD = Decimal("1000")
    HIGH_THRESHOLD = Decimal("10000")
    MATERIALITY_ESCALATION_THRESHOLD = Decimal("0.10")

    # Ranking weights
    FLAGGED_RATIO_WEIGHT = 4
    VOLATILITY_WEIGHT = 0.5
    DUPLICATE_DENSITY_WEIGHT = 2
    RECURRING_WEIGHT = 2
