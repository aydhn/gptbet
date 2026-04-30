from sports_signal_bot.evidence.strategies.base import BaseExplainabilityStrategy
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord
from typing import Dict, Any

class ConservativeAuditStrategy(BaseExplainabilityStrategy):
    def format_bundle(self, bundle: EvidenceBundleRecord) -> Dict[str, Any]:
        result = super().format_bundle(bundle)
        result["strategy"] = "conservative_audit"
        result["claims"] = [c.model_dump() for c in bundle.claims]
        result["citations"] = [c.model_dump() for c in bundle.citations]
        return result
