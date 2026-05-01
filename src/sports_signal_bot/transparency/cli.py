import typer
from datetime import datetime
import json
from .contracts import LogFamily, EventFamily, GossipTopic
from .logs import TransparencyLogManager
from .checkpoints import CheckpointManager
from .mirrors import MirrorManager
from .gossip import GossipManager

app = typer.Typer(help="Phase 56: Governance Transparency")

log_mgr = TransparencyLogManager()
cp_mgr = CheckpointManager()
mirror_mgr = MirrorManager()
gossip_mgr = GossipManager()

@app.command()
def run_transparency_pass():
    """Run transparency pass: generate events, log, seal checkpoint, sync mirror, gossip."""
    typer.echo("Running transparency pass...")

    # 1. Event to log
    payload = {"decision": "approve_model_v2"}
    payload_hash = "mock_payload_hash"

    entry = log_mgr.append_transparency_entry(
        family=LogFamily.GOVERNANCE_DECISION_LOG,
        event_family=EventFamily.CRITICAL_DECISION_PROOF_CREATED,
        event_ref="proof_123",
        payload_hash=payload_hash
    )
    typer.echo(f"Appended entry {entry.transparency_entry_id}")

    # 2. Seal checkpoint
    cp = log_mgr.seal_transparency_checkpoint(LogFamily.GOVERNANCE_DECISION_LOG)
    typer.echo(f"Sealed checkpoint {cp.checkpoint_id} with root {cp.root_hash}")

    # 3. Sign checkpoint
    sig = cp_mgr.sign_checkpoint(cp, signer_set=["signer_1"], signature_block="mock_sig")
    typer.echo(f"Signed checkpoint: {sig.signature_id}")

    # 4. Mirror sync
    mirror = mirror_mgr.create_verification_mirror(family="governance_mirror", source_log_id=cp.log_id)
    sync_rec = mirror_mgr.sync_mirror_from_source(mirror.mirror_id, cp)
    typer.echo(f"Mirror {mirror.mirror_id} synced status: {sync_rec.status}")

    # 5. Gossip
    gossip_env = gossip_mgr.build_gossip_envelope(
        topic=GossipTopic.SIGNED_CHECKPOINT_UPDATES,
        source_plane="plane_alpha",
        details={"checkpoint_id": cp.checkpoint_id, "root_hash": cp.root_hash},
        signature="mock_gossip_sig"
    )
    typer.echo(f"Gossip generated: {gossip_env.envelope_id}")

@app.command()
def preview_transparency_logs():
    """Preview current transparency logs."""
    log = log_mgr.get_log(LogFamily.GOVERNANCE_DECISION_LOG)
    typer.echo(f"Log: {log.log_id}, Entries: {len(log.entries)}, Checkpoints: {len(log.checkpoints)}")
    for e in log.entries:
        typer.echo(f"  - {e.transparency_entry_id} (Status: {e.inclusion_status.value})")

@app.command()
def preview_signed_checkpoints():
    """Preview signed checkpoints."""
    log = log_mgr.get_log(LogFamily.GOVERNANCE_DECISION_LOG)
    for cp in log.checkpoints:
        status = "Signed" if cp.signed_checkpoint_ref else "Unsigned"
        typer.echo(f"CP: {cp.checkpoint_id} - Size: {cp.tree_size} - {status}")

@app.command()
def verify_inclusion_proof(entry_index: int = 0):
    """Verify an inclusion proof for a specific entry index."""
    try:
        # Run pass first to generate data since mgr is stateful
        run_transparency_pass()
        proof = log_mgr.get_inclusion_proof(LogFamily.GOVERNANCE_DECISION_LOG, entry_index)
        typer.echo(f"Generated Proof: {proof.proof_id} for Leaf Index: {proof.leaf_index}")
        typer.echo(f"Merkle Path Size: {len(proof.merkle_path)}")
        typer.echo("Verification: Successful (Mock)")
    except Exception as e:
        typer.echo(f"Error: {e}")

@app.command()
def verify_transparency_mirrors():
    """Verify state of all mirrors."""
    run_transparency_pass()
    for mirror_id, mirror in mirror_mgr._mirrors.items():
        typer.echo(f"Mirror {mirror_id} | Trust: {mirror.trust_status.value} | Latest CP: {mirror.latest_seen_checkpoint}")

@app.command()
def list_transparency_strategies():
    """List available transparency strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeTransparencyStrategy")
    typer.echo("- BalancedVerificationMeshStrategy")
    typer.echo("- MirrorHeavyAuditStrategy")
