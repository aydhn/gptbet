from src.sports_signal_bot.continuity_arbitration_hardening.contracts import ProofMeshReplayRecord
from src.sports_signal_bot.continuity_arbitration_hardening.archive_proof_meshes import build_archive_proof_mesh

def test_build_archive_proof_mesh_success():
    replays = [ProofMeshReplayRecord(replay_id="1", replay_successful=True)]
    mesh = build_archive_proof_mesh("test_mesh", [], replays)
    assert mesh.mesh_status == "mesh_verified"

def test_build_archive_proof_mesh_fail():
    replays = [ProofMeshReplayRecord(replay_id="1", replay_successful=False)]
    mesh = build_archive_proof_mesh("test_mesh", [], replays)
    assert mesh.mesh_status == "mesh_broken"
