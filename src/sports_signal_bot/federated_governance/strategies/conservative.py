from typing import Dict, Any, List
import uuid
from .base import BaseFederatedGovernanceStrategy
from ..contracts import FederatedManifest, ControlPlaneRecord, PlaneSuspensionRecord, PlaneHealthBand

class ConservativeFederatedGovernanceStrategy(BaseFederatedGovernanceStrategy):
    """
    Conservative strategy:
    - Heavy global precedence.
    - Escalates early.
    - More frequent suspensions.
    """

    def evaluate_mesh(self, planes: List[ControlPlaneRecord], context: Dict[str, Any]) -> FederatedManifest:
        escalations = context.get("escalations", [])

        # Suspend noisy planes proactively
        suspensions = []
        for p in planes:
            if p.health in [PlaneHealthBand.NOISY, PlaneHealthBand.STRESSED, PlaneHealthBand.UNSTABLE]:
                p.active_status = False
                suspensions.append(PlaneSuspensionRecord(
                    suspension_id=f"sus_{uuid.uuid4().hex[:8]}",
                    plane_id=p.plane_id,
                    reason="Conservative strategy proactive suspension due to health",
                    active=True
                ))

        manifest = FederatedManifest(
            manifest_id=f"man_{uuid.uuid4().hex[:8]}",
            planes=planes,
            active_escalations=escalations,
            budget_summary={},
            mesh_hotspots=[],
            suspensions=suspensions,
            overrides=[]
        )
        return manifest
