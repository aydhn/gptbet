import typer
import json
from typing import List
from .contracts import (
    FederatedSummaryInput,
    ControlPlaneRecord,
    PlanePrecedence,
    PlaneHealthBand,
    PlaneTrustBand,
    PlaneBudgetRecord,
    EscalationCaseRecord,
    MeshTopologyRecord,
    PlaneSuspensionRecord,
)
from .control_tower import FederatedControlTowerBuilder

app = typer.Typer(
    help=("Phase 52 Federated Governance & " "Control Plane Architecture")
)


def get_mock_planes() -> List[ControlPlaneRecord]:
    return [
        ControlPlaneRecord(
            plane_id="global_plane",
            plane_name="Global Control",
            plane_family="global",
            precedence=PlanePrecedence.GLOBAL_GOVERNANCE,
            active_status=True,
            health=PlaneHealthBand.HEALTHY,
            trust=PlaneTrustBand.HIGH,
        ),
        ControlPlaneRecord(
            plane_id="family_provider",
            plane_name="Provider Governance",
            plane_family="provider",
            precedence=PlanePrecedence.FAMILY_DOMAIN,
            parent_plane_id="global_plane",
            active_status=True,
            health=PlaneHealthBand.STRESSED,
            trust=PlaneTrustBand.MEDIUM,
        ),
        ControlPlaneRecord(
            plane_id="security_cross",
            plane_name="Security Veto Plane",
            plane_family="security",
            precedence=(PlanePrecedence.CROSS_CUTTING_CRITICAL),
            active_status=True,
            health=PlaneHealthBand.HEALTHY,
            trust=PlaneTrustBand.HIGH,
        ),
        ControlPlaneRecord(
            plane_id="noisy_cohort",
            plane_name="Noisy Local Cohort",
            plane_family="cohort",
            precedence=(PlanePrecedence.COHORT_ADOPTION),
            parent_plane_id="family_provider",
            active_status=False,
            health=PlaneHealthBand.SUSPENDED,
            trust=PlaneTrustBand.LOW,
        ),
    ]


@app.command()
def run_federated_governance():
    """Run a federated governance evaluation cycle."""
    typer.echo("Starting Federated Governance Cycle...")
    planes = get_mock_planes()
    budgets = [
        PlaneBudgetRecord(
            budget_id="b1",
            plane_id="global_plane",
            budget_type="risk",
            total_amount=100.0,
            used_amount=20.0,
        ),
        PlaneBudgetRecord(
            budget_id="b2",
            plane_id="family_provider",
            budget_type="risk",
            total_amount=40.0,
            used_amount=35.0,
        ),
    ]
    escalations = [
        EscalationCaseRecord(
            case_id="e1",
            source_plane_id="noisy_cohort",
            target_plane_id="family_provider",
            reason="Budget saturation",
        )
    ]
    topology = MeshTopologyRecord(
        topology_id="t1",
        nodes=["global_plane", "family_provider", "security_cross", "noisy_cohort"],  # noqa: E501
        edges=[
            {
                "source": "noisy_cohort",
                "target": "family_provider",
                "rel": "escalates_to",
            }
        ],
    )
    suspensions = [
        PlaneSuspensionRecord(
            suspension_id="s1", plane_id="noisy_cohort", reason="Too noisy", active=True  # noqa: E501
        )
    ]
    overrides = []

    builder = FederatedControlTowerBuilder()
    input_data = FederatedSummaryInput(
        planes=planes,
        budgets=budgets,
        escalations=escalations,
        topology=topology,
        suspensions=suspensions,
        overrides=overrides,
    )
    summary = builder.build_summary(input_data)

    typer.echo("\n--- Federated Control Tower Summary ---")
    typer.echo(json.dumps(summary, indent=2))
    typer.echo("\nArtifacts updated.")


@app.command()
def preview_control_planes():
    """Preview the active control planes and their hierarchy."""
    planes = get_mock_planes()
    for p in planes:
        typer.echo(
            f"- {p.plane_id} ({p.plane_family}) "
            f"- Precedence: {p.precedence.name} "
            f"- Health: {p.health.value}"
        )


@app.command()
def preview_escalations():
    """Preview current cross-plane escalations."""
    typer.echo("Active Escalations:")
    typer.echo("- noisy_cohort -> family_provider " "(Reason: Budget saturation)")  # noqa: E501


@app.command()
def preview_budget_tree():
    """Preview the federated budget allocations."""
    typer.echo("Budget Tree:")
    typer.echo("- global_plane: 80.0 available")
    typer.echo("- family_provider: 5.0 available " "(WARNING: Highly saturated)")  # noqa: E501


@app.command()
def preview_mesh_topology():
    """Preview the control plane mesh and hotspots."""
    typer.echo("Mesh Topology:")
    typer.echo("Nodes: 4, Edges: 1")
    typer.echo("Hotspots: None detected currently")


@app.command()
def preview_plane_suspensions():
    """Preview planes with reduced autonomy or active suspensions."""
    typer.echo("Plane Suspensions & Autonomy Reductions:")
    typer.echo("- noisy_cohort (Status: SUSPENDED, Reason: Too noisy)")


@app.command()
def list_federated_governance_strategies():
    """List available federated governance strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeFederatedGovernanceStrategy")
    typer.echo("- BalancedFederatedMeshStrategy (Default)")
    typer.echo("- FamilyCentricDelegationStrategy")
    typer.echo("- CrossCuttingFirstStrategy")
    typer.echo("- ThroughputGuardedFederationStrategy")


if __name__ == "__main__":
    app()
