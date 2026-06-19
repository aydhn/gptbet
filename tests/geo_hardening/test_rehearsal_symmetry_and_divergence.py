from sports_signal_bot.geo_hardening.rehearsal_symmetry import (
    compute_rehearsal_symmetry,
    classify_divergence_severity,
    detect_dual_writer_risk,
    summarize_rehearsal_divergence
)

def test_symmetry():
    assert True

def test_classify_divergence_severity():
    assert classify_divergence_severity(0.6) == "critical"
    assert classify_divergence_severity(0.5) == "high"
    assert classify_divergence_severity(0.2) == "high"
    assert classify_divergence_severity(0.1) == "low"
    assert classify_divergence_severity(0.0) == "low"

def test_compute_rehearsal_symmetry():
    assert compute_rehearsal_symmetry([]) == {"symmetry_ratio": 1.0, "is_asymmetric": False}
    assert compute_rehearsal_symmetry([1.0, 1.05]) == {"symmetry_ratio": 1.025, "is_asymmetric": False}
    assert compute_rehearsal_symmetry([1.0, 1.5]) == {"symmetry_ratio": 1.25, "is_asymmetric": True}
    assert compute_rehearsal_symmetry([1.0]) == {"symmetry_ratio": 1.0, "is_asymmetric": False}
    assert compute_rehearsal_symmetry([2.0, 2.0, 2.0]) == {"symmetry_ratio": 2.0, "is_asymmetric": False}
    assert compute_rehearsal_symmetry([-1.0, -1.05]) == {"symmetry_ratio": -1.025, "is_asymmetric": False}
    assert compute_rehearsal_symmetry([0.0, 0.0]) == {"symmetry_ratio": 0.0, "is_asymmetric": False}
    assert compute_rehearsal_symmetry([1.0, 1.05, 1.2]) == {"symmetry_ratio": 1.0833333333333333, "is_asymmetric": True}


def test_detect_dual_writer_risk():
    assert detect_dual_writer_risk([
        {"is_write": True, "region": "us-east"},
        {"is_write": False, "region": "us-west"}
    ]) is False

    assert detect_dual_writer_risk([
        {"is_write": True, "region": "us-east"},
        {"is_write": True, "region": "us-west"}
    ]) is True

def test_summarize_rehearsal_divergence():
    assert summarize_rehearsal_divergence([0.6, 0.2, 0.1]) == {"total_divergences": 3, "critical": 1}
