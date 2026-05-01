from typing import Dict, Any
from .base import VerifierPortalStrategy

class ConservativeVerifierPortalStrategy(VerifierPortalStrategy):
    def apply_strategy(self) -> Dict[str, Any]:
        return {
            "name": "ConservativeVerifierPortalStrategy",
            "default_profile": "public_viewer",
            "strict_challenge_intake": True,
            "feed_freshness_strict": True
        }
