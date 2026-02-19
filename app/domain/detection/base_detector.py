from abc import ABC, abstractmethod
from typing import List

from app.domain.models.transaction import Transaction
from app.domain.models.detection_result import DetectionResult


class BaseDetector(ABC):
    """
    Base contract for all detection modules.

    Guarantees:
    - Deterministic behavior
    - No mutation of input transactions
    - Structured DetectionResult output
    - Version traceability
    """

    VERSION = "1.0.0"

    @abstractmethod
    def detect(self, transactions: List[Transaction]) -> List[DetectionResult]:
        pass

    def detector_metadata(self) -> dict:
        """
        Returns structured metadata for audit traceability.
        """
        return {
            "detector_class": self.__class__.__name__,
            "detector_version": self.VERSION,
        }
