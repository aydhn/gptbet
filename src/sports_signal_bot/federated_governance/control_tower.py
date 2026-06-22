from typing import Dict, Any, List
import uuid
from .contracts import (
    FederatedSummaryInput,
    ControlPlaneRecord,
    PlaneBudgetRecord,
    EscalationCaseRecord,
    MeshTopologyRecord,
)
from .budgets import summarize_budget_tree


class BudgetTreeReporter:
    def report(self, budgets: List[PlaneBudgetRecord]) -> Dict[str, Any]:
        return summarize_budget_tree(budgets)


class EscalationTracker:
    def summarize(self, escalations: List[EscalationCaseRecord]) -> Dict[str, int]:  # noqa: E501
        counts = {}
        for e in escalations:
            counts[e.source_plane_id] = counts.get(e.source_plane_id, 0) + 1
        return counts


class MeshHealthReporter:
    def report(
        self, topology: MeshTopologyRecord, escalations: List[EscalationCaseRecord]  # noqa: E501
    ) -> Dict[str, Any]:
        return {
            "nodes": len(topology.nodes),
            "edges": len(topology.edges),
            "escalation_count": len(escalations),
        }


class GovernanceTopologyReporter:
    def report(self, planes: List[ControlPlaneRecord]) -> Dict[str, Any]:
        return {
            "total_planes": len(planes),
            "healthy_planes": len([p for p in planes if p.health.value == "healthy"]),  # noqa: E501
            "suspended_planes": len(
                [
                    p
                    for p in planes
                    if p.health.value == "suspended" or not p.active_status
                ]
            ),
        }


class FederatedControlTowerBuilder:
    def build_summary(self, input_data: FederatedSummaryInput) -> Dict[str, Any]:  # noqa: E501

        budget_reporter = BudgetTreeReporter()
        escalation_tracker = EscalationTracker()
        mesh_reporter = MeshHealthReporter()
        topology_reporter = GovernanceTopologyReporter()

        return {
            "summary_id": f"fct_{uuid.uuid4().hex[:8]}",
            "governance_topology": topology_reporter.report(input_data.planes),
            "budget_tree": budget_reporter.report(input_data.budgets),
            "escalations": escalation_tracker.summarize(input_data.escalations),  # noqa: E501
            "mesh_health": mesh_reporter.report(
                input_data.topology, input_data.escalations
            ),
            "active_suspensions": len([s for s in input_data.suspensions if s.active]),  # noqa: E501
            "active_overrides": len([o for o in input_data.overrides if o.active]),  # noqa: E501
        }
