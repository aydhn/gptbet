from .base import EvidenceAtlasStrategy
from typing import Dict, Any

class ConservativeEvidenceAtlasStrategy(EvidenceAtlasStrategy):
    """
    - default
    - stale currentness, evidence gaps and narrative caveat losses ağır baskın
    - mesh ve narrative outputs hızlı caveated/stale olur
    - no-safe visibility en yüksek önemde
    """
    def apply_currentness_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['status'] = 'degraded_quickly_on_staleness'
        data['no_safe_visibility_preserved'] = True
        return data

    def apply_mesh_pressure_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['mesh_status'] = 'caveated_quickly'
        return data

    def apply_clearing_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['clearing_status'] = 'strict_evidence_required'
        return data
