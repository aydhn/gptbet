from typing import Dict, Any
from .base import VerifierPortalStrategy

class ProofRichTrustedVerifierStrategy(VerifierPortalStrategy):
    def apply_strategy(self) -> Dict[str, Any]:
        return {
            "name": "ProofRichTrustedVerifierStrategy",
            "default_profile": "trusted_external_verifier",
            "strict_challenge_intake": False,
            "feed_freshness_strict": False
        }
