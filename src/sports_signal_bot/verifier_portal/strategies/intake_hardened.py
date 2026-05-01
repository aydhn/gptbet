from typing import Dict, Any
from .base import VerifierPortalStrategy

class IntakeHardenedVerifierAPI(VerifierPortalStrategy):
    def apply_strategy(self) -> Dict[str, Any]:
        return {
            "name": "IntakeHardenedVerifierAPI",
            "default_profile": "public_viewer",
            "strict_challenge_intake": True,
            "feed_freshness_strict": False
        }
