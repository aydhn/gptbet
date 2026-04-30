from sports_signal_bot.evidence.strategies.base import BaseExplainabilityStrategy
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord
from typing import Dict, Any

class OperatorConciseStrategy(BaseExplainabilityStrategy):
    def format_bundle(self, bundle: EvidenceBundleRecord) -> Dict[str, Any]:
        result = super().format_bundle(bundle)
        result["strategy"] = "operator_concise"
        result["key_reasons"] = [c.claim_text for c in bundle.claims if c.support_strength in ["high", "medium"]]
        return result
