from decimal import Decimal
from typing import List, Dict
import copy
import json

from app.domain.models.transaction import Transaction
from app.domain.detection.duplicate_detector import DuplicateDetector
from app.domain.detection.recurring_detector import RecurringDetector
from app.domain.scoring.risk_scoring import RiskScoringEngine
from app.domain.utils.dataset_fingerprint import generate_dataset_hash
from app.domain.behavior.vendor_behavior_analyzer import VendorBehaviorAnalyzer
from app.domain.ranking.vendor_risk_ranker import VendorRiskRanker


ENGINE_VERSION = "0.4.0"


class VendorLeakEngine:

    def __init__(self, enforce_determinism: bool = False):
        self.detectors = [
            DuplicateDetector(),
            RecurringDetector(),
        ]
        self.scoring_engine = RiskScoringEngine()
        self.behavior_analyzer = VendorBehaviorAnalyzer()
        self.vendor_ranker = VendorRiskRanker()
        self.enforce_determinism = enforce_determinism

    def run(self, transactions: List[Transaction]) -> Dict:

        result = self._execute(transactions)

        if self.enforce_determinism:
            verification = self._execute(copy.deepcopy(transactions))

            if json.dumps(result, sort_keys=True, default=str) != \
               json.dumps(verification, sort_keys=True, default=str):
                raise RuntimeError("Determinism violation detected")

        return result

    def _execute(self, transactions: List[Transaction]) -> Dict:

        dataset_hash = generate_dataset_hash(transactions)

        all_detections = []
        for detector in self.detectors:
            results = detector.detect(transactions)
            all_detections.extend(results)

        total_spend_by_currency = self._calculate_total_spend(transactions)

        scored_results = self.scoring_engine.score(
            detections=all_detections,
            total_spend_by_currency=total_spend_by_currency,
        )

        sorted_detections = sorted(
            scored_results["updated_detections"],
            key=lambda d: (
                d.detection_type.value,
                d.currency,
                str(d.financial_impact_estimate),
                sorted(d.related_transaction_ids),
            )
        )

        vendor_behavior_profiles = self.behavior_analyzer.analyze(transactions)

        vendor_ranking = self.vendor_ranker.rank(
            scored_results["vendor_totals"],
            vendor_behavior_profiles,
            total_spend_by_currency,
        )

        return {
            "engine_version": ENGINE_VERSION,
            "dataset_hash": dataset_hash,
            "detections": sorted_detections,
            "vendor_totals": scored_results["vendor_totals"],
            "currency_totals": scored_results["currency_totals"],
            "summary": scored_results["summary"],
            "vendor_behavior_profiles": vendor_behavior_profiles,
            "vendor_ranking": vendor_ranking,
        }

    def _calculate_total_spend(self, transactions: List[Transaction]) -> Dict[str, Decimal]:
        totals: Dict[str, Decimal] = {}

        for tx in transactions:
            totals.setdefault(tx.currency, Decimal("0"))
            totals[tx.currency] += tx.amount

        return totals
