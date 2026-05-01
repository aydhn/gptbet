from typing import Dict, Any
from .base import VerifierPortalStrategy

class QuarantineFirstPortalStrategy(VerifierPortalStrategy):
    def apply_strategy(self) -> Dict[str, Any]:
        return {
            "name": "QuarantineFirstPortalStrategy",
            "default_profile": "quarantine_reviewer",
            "strict_challenge_intake": True,
            "feed_freshness_strict": True,
            "quarantine_all_unknown": True
        }
