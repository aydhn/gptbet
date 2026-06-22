import pytest

from sports_signal_bot.geo_hardening.active_active import (
    build_active_active_rehearsal, detect_rehearsal_divergence)
from sports_signal_bot.geo_hardening.rehearsal_symmetry import (
    classify_divergence_severity, compute_rehearsal_symmetry,
    detect_dual_writer_risk)


def test_active_active_asymmetry_set():
    # Active-active asymmetry set
    metrics = [1.0, 1.05, 0.95, 1.2]
    sym = compute_rehearsal_symmetry(metrics)
    assert sym["is_asymmetric"] is True

    events = [
        {"region": "us-east", "is_write": True},
        {"region": "us-west", "is_write": True},
    ]
    assert detect_dual_writer_risk(events) is True

    rehearsal = build_active_active_rehearsal(
        "reh-1", "dual_region_active_active_rehearsal"
    )
    rehearsal = detect_rehearsal_divergence(rehearsal, "div-1")
    assert rehearsal.rehearsal_status == "rehearsal_caveated"

    assert classify_divergence_severity(0.6) == "critical"
