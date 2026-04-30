from typing import Dict, Any, List
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord

class BaseExplainabilityStrategy:
    def format_bundle(self, bundle: EvidenceBundleRecord) -> Dict[str, Any]:
        return {
            "bundle_id": bundle.bundle_id,
            "target": bundle.target_entity_id,
            "confidence": bundle.confidence_band,
            "claims_count": len(bundle.claims)
        }
