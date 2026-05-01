from sports_signal_bot.governance_integrity.canonicalization import (
    canonicalize_for_signing,
    compute_hash,
    validate_canonicalization_stability
)

def test_canonicalization_stability():
    payload = {"b": 2, "a": 1, "c": {"z": 9, "x": 8}}
    assert validate_canonicalization_stability(payload)

def test_canonicalization_sorting():
    p1 = {"a": 1, "b": 2}
    p2 = {"b": 2, "a": 1}
    assert compute_hash(p1) == compute_hash(p2)
