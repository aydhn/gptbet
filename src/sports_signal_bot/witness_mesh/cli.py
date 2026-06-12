import datetime
from typing import List

import typer

from .adjudication import AdjudicationEngine
from .anomalies import AnomalyDetector
from .challenges import ChallengeEngine
from .consensus import ConsensusEngine
from .contracts import (
    AnomalyAdjudicationOutcome,
    WitnessCapability,
    WitnessFamily,
    WitnessNodeRecord,
    WitnessStatementRecord,
    WitnessStatementType,
)
from .readiness import ReadinessScorer
from .witnesses import WitnessMeshBuilder

app = typer.Typer(help="Phase 57 Witness Mesh and Audit Readiness")


def get_mock_nodes() -> List[WitnessNodeRecord]:
    return [
        WitnessNodeRecord(
            witness_id="w1",
            witness_name="local_verifier_1",
            witness_family=WitnessFamily.LOCAL_WITNESS,
            trust_role="internal_auditor",
            verification_capabilities=[WitnessCapability.VERIFY_CHECKPOINT],
            observed_log_families=["stable_adoption"],
            active_status="active",
            freshness_window={"max_age_hours": 24},
        ),
        WitnessNodeRecord(
            witness_id="w2",
            witness_name="mirror_watcher_1",
            witness_family=WitnessFamily.MIRROR_WITNESS,
            trust_role="external_observer",
            verification_capabilities=[
                WitnessCapability.VERIFY_CHECKPOINT,
                WitnessCapability.ISSUE_CHALLENGE,
            ],
            observed_log_families=["stable_adoption", "policy_promotion"],
            active_status="active",
            freshness_window={"max_age_hours": 12},
        ),
    ]


def _build_and_report_mesh(nodes: List[WitnessNodeRecord]):
    builder = WitnessMeshBuilder()
    mesh = builder.build_witness_mesh(nodes)
    coverage = builder.compute_witness_coverage(
        mesh, ["stable_adoption/v1", "policy_promotion/v2"]
    )

    typer.echo(f"Built Mesh with {len(mesh.nodes)} nodes.")
    for cov in coverage:
        msg = f"Coverage for {cov.target_ref}: "
        msg += f"{len(cov.witness_ids)} witnesses"
        typer.echo(msg)


def _generate_mock_statements() -> List[WitnessStatementRecord]:
    return [
        WitnessStatementRecord(
            statement_id="stmt1",
            witness_id="w1",
            statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="stable_adoption/v1",
            target_hash="hashA",
            observed_status="ok",
            observation_window={},
            verification_result="confirmed",
            created_at=datetime.datetime.now(datetime.timezone.utc),
        ),
        WitnessStatementRecord(
            statement_id="stmt2",
            witness_id="w2",
            statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="stable_adoption/v1",
            target_hash="hashA",
            observed_status="ok",
            observation_window={},
            verification_result="confirmed",
            created_at=datetime.datetime.now(datetime.timezone.utc),
        ),
        WitnessStatementRecord(
            statement_id="stmt3",
            witness_id="w2",
            statement_family=WitnessStatementType.CHECKPOINT_VERIFIED,
            target_ref="policy_promotion/v2",
            target_hash="hashB",
            observed_status="mismatch",
            observation_window={},
            verification_result="rejected",
            created_at=datetime.datetime.now(datetime.timezone.utc),
        ),
    ]


def _compute_and_report_consensus(statements: List[WitnessStatementRecord]):
    consensus_engine = ConsensusEngine()
    ref = "stable_adoption/v1"
    cons1 = consensus_engine.compute_witness_consensus(statements, ref)
    cons2 = consensus_engine.compute_witness_consensus(
        statements, "policy_promotion/v2"
    )

    msg1 = f"Consensus for stable_adoption/v1: {cons1.consensus_type.value}"
    typer.echo(msg1)
    msg2 = f"Consensus for policy_promotion/v2: {cons2.consensus_type.value}"
    typer.echo(msg2)
    return cons1, cons2


def _process_challenges_and_anomalies():
    challenge_engine = ChallengeEngine()
    anomaly_detector = AnomalyDetector()
    adj_engine = AdjudicationEngine()

    challenge = challenge_engine.issue_challenge(
        "w2", "policy_promotion/v2", "hash mismatch detected"
    )
    typer.echo(
        f"Issued Challenge: {challenge.challenge_id} | "
        f"status: {challenge.current_status.value}"
    )

    anomaly = anomaly_detector.detect_anomalies(
        "policy_promotion/v2", "hash mismatch", ["w2"]
    )
    typer.echo(f"Detected Anomaly: {anomaly.anomaly_type.value}")

    adj = adj_engine.adjudicate_transparency_anomaly(
        anomaly,
        AnomalyAdjudicationOutcome.LOCAL_MIRROR_ISSUE,
        "mirror was stale",
    )
    typer.echo(f"Adjudicated Anomaly: {adj.outcome.value}")
    return challenge, anomaly


def _compute_and_report_readiness(cons1, cons2, challenge, anomaly):
    readiness_scorer = ReadinessScorer()
    readiness = readiness_scorer.compute_public_style_readiness(
        [cons1, cons2], [challenge], [anomaly]
    )

    typer.echo("\n--- Public-Style Readiness ---")
    typer.echo(f"Status: {readiness.status.value}")
    typer.echo(f"Score: {readiness.dimension_scores.get('overall', 0)}")
    if readiness.blockers:
        typer.echo("Blockers:")
        for b in readiness.blockers:
            typer.echo(f" - {b}")


@app.command("run-witness-mesh-pass")
def run_witness_mesh_pass():
    """Run complete witness mesh, consensus, challenge, and readiness pass."""
    typer.echo("Starting Witness Mesh Pass...")
    nodes = get_mock_nodes()

    _build_and_report_mesh(nodes)
    statements = _generate_mock_statements()
    cons1, cons2 = _compute_and_report_consensus(statements)
    challenge, anomaly = _process_challenges_and_anomalies()

    _compute_and_report_readiness(cons1, cons2, challenge, anomaly)


@app.command("preview-witness-nodes")
def preview_witness_nodes():
    nodes = get_mock_nodes()
    for n in nodes:
        typer.echo(
            f"Node: {n.witness_id} | Family: {n.witness_family.value} | "
            f"Role: {n.trust_role}"
        )


@app.command("preview-public-style-readiness")
def preview_readiness():
    scorer = ReadinessScorer()
    # mock empty to show perfect score
    readiness = scorer.compute_public_style_readiness([], [], [])
    typer.echo(f"Status: {readiness.status.value}")
    typer.echo(f"Score: {readiness.dimension_scores.get('overall', 0)}")


if __name__ == "__main__":
    app()
