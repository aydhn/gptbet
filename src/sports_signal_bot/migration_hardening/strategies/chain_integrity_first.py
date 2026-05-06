from typing import Dict, Any
from .base import BaseMigrationHardeningStrategy

class ChainIntegrityFirstStrategy(BaseMigrationHardeningStrategy):
    """
    archival chain integrity, lineage continuity and restore dependency correctness dominant
    """
    def evaluate_migration_readiness(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "ChainIntegrityFirst", "is_release_blocking": False}

    def evaluate_coordination(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "ChainIntegrityFirst", "is_release_blocking": False}

    def evaluate_recovery_chain(self, context: Dict[str, Any]) -> Dict[str, Any]:
        chain = context.get('chain')
        if not chain: return {"status": "error"}
        is_blocked = chain.chain_status not in ["chain_verified", "chain_review_only"]
        return {
             "strategy": "ChainIntegrityFirst",
             "is_release_blocking": is_blocked,
             "chain_status": chain.chain_status.value
        }

    def evaluate_visibility_wargame(self, context: Dict[str, Any]) -> Dict[str, Any]:
         return {"strategy": "ChainIntegrityFirst", "is_release_blocking": False}
