from abc import ABC, abstractmethod
from typing import List

from app.domain.models.transaction import Transaction
from app.domain.models.detection_result import DetectionResult


class BaseDetector(ABC):

    @abstractmethod
    def detect(self, transactions: List[Transaction]) -> List[DetectionResult]:
        """
        Must be deterministic.
        Must not mutate input transactions.
        Must return structured DetectionResult objects.
        """
        pass
