import uuid
from typing import List, Dict, Any
from sports_signal_bot.distributed_coordination.contracts import TenancyIsolationRecord

class TenancyIsolationManager:
    """Manages tenant and domain isolation boundaries."""

    def build_tenancy_isolation_policy(self, tenant_ref: str, allowed_lanes: List[str]) -> TenancyIsolationRecord:
        """Builds a new Tenancy Isolation policy record."""
        return TenancyIsolationRecord(
            isolation_id=f"isolation_{uuid.uuid4().hex[:8]}",
            tenant_or_domain_ref=tenant_ref,
            allowed_lane_families=allowed_lanes,
            forbidden_shared_surfaces=["global_rollback_cache", "root_closure_pool"],
            token_scope_policy="strict_namespace_isolation",
            approval_boundary_policy="tenant_scoped_only",
            visibility_boundary_policy="tenant_visibility_only",
            warnings=[]
        )

    def validate_cross_tenant_requests(self, isolation_policy: TenancyIsolationRecord, requested_surface: str) -> bool:
        """Returns True if the request is valid (does not cross forbidden surfaces)."""
        if requested_surface in isolation_policy.forbidden_shared_surfaces:
            return False
        return True

    def segment_runtime_visibility(self, isolation_policy: TenancyIsolationRecord, all_lanes: List[str], lane_tenant_mapping: Dict[str, str]) -> List[str]:
        """Filters a list of lanes to only those visible to the tenant."""
        visible_lanes = []
        for lane in all_lanes:
            if lane_tenant_mapping.get(lane) == isolation_policy.tenant_or_domain_ref:
                visible_lanes.append(lane)
        return visible_lanes

    def explain_isolation_blocks(self, isolation_policy: TenancyIsolationRecord, blocked_surface: str) -> str:
        """Provides human-readable reasoning for an isolation block."""
        return f"Access to surface '{blocked_surface}' blocked for tenant '{isolation_policy.tenant_or_domain_ref}' due to strict namespace isolation policy."
