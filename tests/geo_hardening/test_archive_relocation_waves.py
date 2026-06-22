from sports_signal_bot.geo_hardening.relocation_waves import (
    build_archive_relocation_wave, summarize_archive_relocation_wave,
    verify_relocation_wave_hashes, verify_relocation_wave_lineage,
    verify_relocation_wave_replay_support)
from sports_signal_bot.geo_hardening.wave_checkpoints import (
    detect_relocation_wave_gaps, diff_relocation_wave_outputs)


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


def test_verify_relocation_wave_hashes():
    wave = build_archive_relocation_wave("wave-1", "archive_seed_wave")
    result = verify_relocation_wave_hashes(wave, "hash-1")
    assert result is True
    assert "hash-1" in wave.hash_refs
    assert len(wave.hash_refs) == 1


def test_verify_relocation_wave_lineage():
    wave = build_archive_relocation_wave("wave-1", "archive_seed_wave")
    result = verify_relocation_wave_lineage(wave, "lineage-1")
    assert result is True
    assert "lineage-1" in wave.lineage_refs
    assert len(wave.lineage_refs) == 1


def test_verify_relocation_wave_replay_support():
    wave = build_archive_relocation_wave("wave-1", "archive_seed_wave")
    result = verify_relocation_wave_replay_support(wave, "replay-1")
    assert result is True
    assert "replay-1" in wave.replay_refs
    assert len(wave.replay_refs) == 1


def test_build_archive_relocation_wave():
    wave = build_archive_relocation_wave("test-wave-id", "test-family")
    assert wave.relocation_wave_id == "test-wave-id"
    assert wave.wave_family == "test-family"
    assert wave.wave_status == "wave_verified"
    assert wave.hash_refs == []


def test_summarize_archive_relocation_wave():
    wave = build_archive_relocation_wave("wave-1", "archive_seed_wave")
    verify_relocation_wave_hashes(wave, "hash-1")
    verify_relocation_wave_lineage(wave, "lineage-1")
    summary = summarize_archive_relocation_wave(wave)
    assert summary == {
        "wave_id": "wave-1",
        "status": "wave_verified",
        "hashes": 1,
        "lineage": 1,
    }


def test_summarize_archive_relocation_wave_empty():
    wave = build_archive_relocation_wave("wave-2", "archive_empty_wave")
    summary = summarize_archive_relocation_wave(wave)
    assert summary == {
        "wave_id": "wave-2",
        "status": "wave_verified",
        "hashes": 0,
        "lineage": 0,
    }


def test_summarize_archive_relocation_wave_multiple():
    wave = build_archive_relocation_wave("wave-3", "archive_multi_wave")
    verify_relocation_wave_hashes(wave, "hash-1")
    verify_relocation_wave_hashes(wave, "hash-2")
    verify_relocation_wave_lineage(wave, "lineage-1")
    verify_relocation_wave_lineage(wave, "lineage-2")
    verify_relocation_wave_lineage(wave, "lineage-3")
    summary = summarize_archive_relocation_wave(wave)
    assert summary == {
        "wave_id": "wave-3",
        "status": "wave_verified",
        "hashes": 2,
        "lineage": 3,
    }
