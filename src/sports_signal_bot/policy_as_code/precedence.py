from typing import List, Dict, Any, Optional
from .contracts import PolicyPrecedenceRecord

class PrecedenceResolver:
    def __init__(self, default_order: List[str] = None):
        if default_order is None:
            self.default_order = [
                "emergency_policy",
                "global_safety",
                "cross_cutting_security",
                "global_governance",
                "family_domain",
                "cohort_adoption",
                "candidate_local",
                "advisory"
            ]
        else:
            self.default_order = default_order

    def resolve_precedence(self, rule_families: List[str]) -> List[str]:
        """Sorts rule families based on precedence order. Lower index = higher precedence."""
        def get_rank(family: str) -> int:
            try:
                return self.default_order.index(family)
            except ValueError:
                return len(self.default_order) # Unknown families have lowest precedence

        return sorted(rule_families, key=get_rank)

    def explain_precedence_resolution(self, resolved_order: List[str]) -> str:
        return f"Precedence order applied: {' -> '.join(resolved_order)}"

    def block_ambiguous_precedence(self, families: List[str]) -> bool:
        """Returns True if there are multiple unknown families, leading to ambiguity."""
        unknowns = [f for f in families if f not in self.default_order]
        return len(unknowns) > 1

    def detect_shadowed_rules(self, active_rules: List[Dict[str, Any]]) -> List[str]:
        # Simplified for now: just return empty list. Full implementation would
        # check if a higher precedence rule completely covers a lower precedence one.
        return []
