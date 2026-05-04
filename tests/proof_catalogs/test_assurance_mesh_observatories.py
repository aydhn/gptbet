import pytest
from src.sports_signal_bot.proof_catalogs.mesh_observatories import (
    build_assurance_mesh_observatory,
    capture_observatory_snapshot
)

def test_build_observatory():
    obs = build_assurance_mesh_observatory("bounded_assurance_mesh_observatory")
    assert obs.observatory_family == "bounded_assurance_mesh_observatory"

def test_capture_snapshot():
    snapshot = capture_observatory_snapshot("mesh_1")
    assert snapshot.source_mesh_ref == "mesh_1"
    assert snapshot.currentness_state == "current"
