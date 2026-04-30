from sports_signal_bot.evidence.strategies.base import BaseExplainabilityStrategy
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord
from typing import Dict, Any

class BalancedReviewStrategy(BaseExplainabilityStrategy):
    def format_bundle(self, bundle: EvidenceBundleRecord) -> Dict[str, Any]:
        result = super().format_bundle(bundle)
        result["strategy"] = "balanced_review"
        result["reasons"] = [c.claim_text for c in bundle.claims]
        result["caveats"] = list({cav for c in bundle.claims for cav in c.caveats})
        return result
