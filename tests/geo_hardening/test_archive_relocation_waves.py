import pytest
from sports_signal_bot.geo_hardening.relocation_waves import build_archive_relocation_wave, verify_relocation_wave_hashes
from sports_signal_bot.geo_hardening.wave_checkpoints import detect_relocation_wave_gaps, diff_relocation_wave_outputs

def test_archive_relocation_wave_lineage_set():
    # Archive relocation wave lineage set
    wave = build_archive_relocation_wave("wave-1", "archive_seed_wave")
    verify_relocation_wave_hashes(wave, "hash-1")
    assert len(wave.hash_refs) == 1

    segments = [{"id": 0}, {"id": 1}, {"id": 3}]
    gaps = detect_relocation_wave_gaps(segments)
    assert gaps == [2]

def test_broken_wave_rollback_readiness_set():
    source = {"data_a": "1", "data_b": "2"}
    target = {"data_a": "1", "data_b": "3"}
    diff = diff_relocation_wave_outputs(source, target)
    assert "data_b" in diff
