from typing import Dict, Any, List, Optional
import uuid
from .contracts import (
    ControlPlaneRecord, PlaneBudgetRecord, EscalationCaseRecord,
    MeshTopologyRecord, PlaneSuspensionRecord, EmergencyOverrideRecord
)
from .budgets import summarize_budget_tree

class BudgetTreeReporter:
    def report(self, budgets: List[PlaneBudgetRecord]) -> Dict[str, Any]:
        return summarize_budget_tree(budgets)

class EscalationTracker:
    def summarize(self, escalations: List[EscalationCaseRecord]) -> Dict[str, int]:
        counts = {}
        for e in escalations:
            counts[e.source_plane_id] = counts.get(e.source_plane_id, 0) + 1
        return counts

class MeshHealthReporter:
    def report(self, topology: MeshTopologyRecord, escalations: List[EscalationCaseRecord]) -> Dict[str, Any]:
        return {
            "nodes": len(topology.nodes),
            "edges": len(topology.edges),
            "escalation_count": len(escalations)
        }

class GovernanceTopologyReporter:
    def report(self, planes: List[ControlPlaneRecord]) -> Dict[str, Any]:
        return {
            "total_planes": len(planes),
            "healthy_planes": len([p for p in planes if p.health.value == "healthy"]),
            "suspended_planes": len([p for p in planes if p.health.value == "suspended" or not p.active_status])
        }

class FederatedControlTowerBuilder:
    def build_summary(self,
                      planes: List[ControlPlaneRecord],
                      budgets: List[PlaneBudgetRecord],
                      escalations: List[EscalationCaseRecord],
                      topology: MeshTopologyRecord,
                      suspensions: List[PlaneSuspensionRecord],
                      overrides: List[EmergencyOverrideRecord]) -> Dict[str, Any]:

        budget_reporter = BudgetTreeReporter()
        escalation_tracker = EscalationTracker()
        mesh_reporter = MeshHealthReporter()
        topology_reporter = GovernanceTopologyReporter()

        return {
            "summary_id": f"fct_{uuid.uuid4().hex[:8]}",
            "governance_topology": topology_reporter.report(planes),
            "budget_tree": budget_reporter.report(budgets),
            "escalations": escalation_tracker.summarize(escalations),
            "mesh_health": mesh_reporter.report(topology, escalations),
            "active_suspensions": len([s for s in suspensions if s.active]),
            "active_overrides": len([o for o in overrides if o.active])
        }
