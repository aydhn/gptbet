from .base import EvidenceAtlasStrategy
from typing import Dict, Any

class ReplayClearingCouncilFirstStrategy(EvidenceAtlasStrategy):
    """
    - replay evidence, bounded clearing and council precedence baskın
    - weak matches hızla review_only/no_safe olur
    - board caps daha görünür olur
    """
    def apply_currentness_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['status'] = 'clearing_council_driven'
        data['no_safe_visibility_preserved'] = True
        return data

    def apply_mesh_pressure_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['mesh_status'] = 'board_caps_visible'
        return data

    def apply_clearing_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['clearing_status'] = 'review_only_on_weak_match'
        return data
