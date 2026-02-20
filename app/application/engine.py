from decimal import Decimal
from typing import List, Dict

from app.domain.models.transaction import Transaction
from app.domain.detection.duplicate_detector import DuplicateDetector
from app.domain.detection.recurring_detector import RecurringDetector
from app.domain.scoring.risk_scoring import RiskScoringEngine
from app.domain.utils.dataset_fingerprint import generate_dataset_hash
from app.domain.behavior.vendor_behavior_analyzer import VendorBehaviorAnalyzer
from app.domain.ranking.vendor_risk_ranker import VendorRiskRanker


ENGINE_VERSION = "0.3.0"


class VendorLeakEngine:

    def __init__(self):
        self.detectors = [
            DuplicateDetector(),
            RecurringDetector(),
        ]
        self.scoring_engine = RiskScoringEngine()
        self.behavior_analyzer = VendorBehaviorAnalyzer()
        self.vendor_ranker = VendorRiskRanker()

    def run(self, transactions: List[Transaction]) -> Dict:

        # Generate deterministic dataset fingerprint
        dataset_hash = generate_dataset_hash(transactions)

        # Run detection modules
        all_detections = []
        for detector in self.detectors:
            results = detector.detect(transactions)
            all_detections.extend(results)

        # Calculate total spend per currency
        total_spend_by_currency = self._calculate_total_spend(transactions)

        # Apply centralized scoring
        scored_results = self.scoring_engine.score(
            detections=all_detections,
            total_spend_by_currency=total_spend_by_currency,
        )

        # Deterministic detection ordering
        sorted_detections = sorted(
            scored_results["updated_detections"],
            key=lambda d: (
                d.detection_type.value,
                d.currency,
                str(d.financial_impact_estimate),
                sorted(d.related_transaction_ids),
            )
        )

        # Compute vendor behavioral fingerprints
        vendor_behavior_profiles = self.behavior_analyzer.analyze(transactions)

        # Compute vendor risk ranking
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
