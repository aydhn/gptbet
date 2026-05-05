import pytest
from sports_signal_bot.hardening.reproducibility import normalize_artifact_for_repro

def test_normalize_artifact():
    art = {"b": 2, "a": 1}
    norm = normalize_artifact_for_repro(art)
    assert list(norm.keys()) == ["a", "b"]
