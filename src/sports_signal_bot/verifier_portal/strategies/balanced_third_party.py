from typing import Dict, Any
from .base import VerifierPortalStrategy

class BalancedThirdPartyVerificationStrategy(VerifierPortalStrategy):
    def apply_strategy(self) -> Dict[str, Any]:
        return {
            "name": "BalancedThirdPartyVerificationStrategy",
            "default_profile": "registered_verifier",
            "strict_challenge_intake": False,
            "feed_freshness_strict": False
        }
