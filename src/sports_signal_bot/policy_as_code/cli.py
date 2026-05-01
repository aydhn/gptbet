import typer
import json
from .evaluation import PolicyEngine
from .contracts import PolicyBundleRecord, PolicyRuleRecord, PolicyOverlayRecord, PolicyReviewStatus
from .diffing import PolicyDiffEngine
from .reviews import PolicyReviewPipeline
from .manifests import generate_manifest, dump_manifest

app = typer.Typer(help="Phase 53 Policy as Code Engine")

def setup_mock_engine() -> PolicyEngine:
    engine = PolicyEngine()

    # Mock Rule 1: Safety block on high pressure
    rule1 = PolicyRuleRecord(
        rule_id="r1_safety_pressure",
        rule_family="global_safety",
        title="Block on Critical Pressure",
        description="Deny any growth if global pressure is critical.",
        priority=10,
        conditions=[{"namespace": "global", "field": "pressure_band", "operator": "==", "value": "critical"}],
        actions=[{"action_type": "deny"}]
    )

    # Mock Rule 2: Cohort requires 2 clean windows
    rule2 = PolicyRuleRecord(
        rule_id="r2_cohort_clean_windows",
        rule_family="cohort_adoption",
        title="Require Clean Windows",
        description="Hold progression if clean windows < 2.",
        priority=50,
        conditions=[{"namespace": "cohort.verification", "field": "clean_windows", "operator": "<", "value": 2}],
        actions=[{"action_type": "hold"}]
    )

    engine.registry.register_rule(rule1)
    engine.registry.register_rule(rule2)

    # Mock Bundle
    bundle1 = PolicyBundleRecord(
        policy_bundle_id="b1_base_governance",
        bundle_name="Base Governance Rules",
        bundle_family="governance",
        version="v1.0.0",
        status=PolicyReviewStatus.ACTIVE,
        rules=["r1_safety_pressure", "r2_cohort_clean_windows"]
    )
    engine.registry.register_bundle(bundle1)

    return engine

@app.command()
def run_policy_evaluation():
    """Run a policy evaluation against a mock context."""
    engine = setup_mock_engine()

    context = {
        "global": {"pressure_band": "moderate"},
        "cohort": {"verification": {"clean_windows": 1}}
    }

    typer.echo(f"Evaluating context: {json.dumps(context)}")

    eval_record = engine.evaluate(context, ["b1_base_governance"])

    typer.echo("\n--- Policy Evaluation Result ---")
    typer.echo(f"Decision Status: {eval_record.decision.decision_status.value}")
    if eval_record.decision.blockers:
        typer.echo("Blockers:")
        for b in eval_record.decision.blockers:
            typer.echo(f"  - {b}")
    typer.echo(f"Triggered Rules: {eval_record.decision.triggered_rules}")
    typer.echo(f"Explanation: {eval_record.decision.policy_explanation}")

    # Generate Manifest
    manifest = generate_manifest(["b1_base_governance"], [], 0, 0)
    dump_manifest(manifest)
    typer.echo("\nManifest dumped to policy_as_code_manifest.json")


@app.command()
def preview_policy_bundles():
    """Preview registered policy bundles."""
    engine = setup_mock_engine()
    typer.echo("Active Policy Bundles:")
    for b_id, bundle in engine.registry.bundles.items():
        typer.echo(f"- {b_id} ({bundle.bundle_name}) - Status: {bundle.status.value}")
        typer.echo(f"  Rules: {bundle.rules}")

@app.command()
def preview_policy_diffs():
    """Preview diffs between two mock bundles."""
    engine = setup_mock_engine()
    b1 = engine.registry.bundles["b1_base_governance"]

    b2 = PolicyBundleRecord(
        policy_bundle_id="b2_proposed",
        bundle_name="Proposed Governance",
        bundle_family="governance",
        version="v1.1.0",
        rules=["r1_safety_pressure"] # Removed r2
    )

    diff_engine = PolicyDiffEngine(engine.registry.rules)
    diff = diff_engine.diff_policy_bundles(b1, b2)

    typer.echo("Policy Diff Summary:")
    typer.echo(diff.human_readable_summary)
    for hint in diff.risk_hints:
        typer.echo(f"Risk Hint: {hint}")

@app.command()
def preview_policy_change_requests():
    """Preview policy change request pipeline."""
    pipeline = PolicyChangeRequestPipeline() # Local mock usage
    req = pipeline.create_change_request("b1_base", {"remove": ["r2_cohort"]}, ["global"])

    typer.echo("Pending Change Requests:")
    typer.echo(f"- {req.request_id} (Bundle: {req.bundle_id}) - Status: {req.status}")

    review = pipeline.submit_review(req.request_id, "reviewer_x", "approve", {"safety_checked": True}, "Looks good")
    typer.echo(f"\nReview Submitted: {review.review_id} (Decision: {review.decision})")
    typer.echo(f"Request Status updated to: {pipeline.requests[req.request_id].status}")

class PolicyChangeRequestPipeline(PolicyReviewPipeline):
    pass

@app.command()
def preview_policy_conflicts():
    """Preview simulated policy conflicts."""
    typer.echo("Simulated Policy Conflicts:")
    typer.echo("- Conflict c_123: r1_safety_pressure (deny) vs r3_emergency_override (permit)")
    typer.echo("  Resolution: r3_emergency_override (based on emergency_policy precedence)")

@app.command()
def preview_applied_policies():
    """Preview immutable applied policy snapshots."""
    typer.echo("Applied Policy Snapshots (Immutable):")
    typer.echo("- Snapshot ap_xyz123 (Bundle Hash: a1b2c3d4)")
    typer.echo("  Context: ctx_456")
    typer.echo("  Evaluated At: 2023-10-27T10:00:00Z")

@app.command()
def list_policy_as_code_strategies():
    """List available Policy-as-Code strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativePolicyAsCodeStrategy")
    typer.echo("- BalancedPolicyMeshStrategy (Default)")
    typer.echo("- OverlayMinimizingStrategy")
    typer.echo("- GovernanceHeavyReviewStrategy")
    typer.echo("- SimulationFirstPolicyStrategy")

if __name__ == "__main__":
    app()
