import pytest
from src.sports_signal_bot.planetary_federation_hardening.corridor_superchains import (
    build_corridor_superchain, add_superchain_segment, verify_corridor_superchain, replay_corridor_superchain,
    SuperchainFamily, SuperchainStatus, SuperchainSegmentRecord, SuperchainReplayRecord, SuperchainLineageRecord
)

def test_verify_corridor_superchain_verified():
    sc = build_corridor_superchain("sc-01", SuperchainFamily.INTERCONTINENTAL_ARCHIVE_SUPERCHAIN)
    add_superchain_segment(sc, SuperchainSegmentRecord("seg-01", is_stale=False))
    sc.replay_refs.append(SuperchainReplayRecord("replay-01", is_supported=True))
    sc.lineage_refs.append(SuperchainLineageRecord("lin-01", preserved=True))

    health = verify_corridor_superchain(sc)
    assert health.is_healthy
    assert health.status == SuperchainStatus.SUPERCHAIN_VERIFIED
    assert replay_corridor_superchain(sc) is True

def test_verify_corridor_superchain_stale():
    sc = build_corridor_superchain("sc-01", SuperchainFamily.INTERCONTINENTAL_ARCHIVE_SUPERCHAIN)
    add_superchain_segment(sc, SuperchainSegmentRecord("seg-01", is_stale=True))
    sc.replay_refs.append(SuperchainReplayRecord("replay-01", is_supported=True))
    sc.lineage_refs.append(SuperchainLineageRecord("lin-01", preserved=True))

    health = verify_corridor_superchain(sc)
    assert not health.is_healthy
    assert health.status == SuperchainStatus.SUPERCHAIN_CAVEATED
    assert replay_corridor_superchain(sc) is False

def test_verify_corridor_superchain_broken():
    sc = build_corridor_superchain("sc-01", SuperchainFamily.INTERCONTINENTAL_ARCHIVE_SUPERCHAIN)
    add_superchain_segment(sc, SuperchainSegmentRecord("seg-01", is_stale=False))
    sc.replay_refs.append(SuperchainReplayRecord("replay-01", is_supported=False))
    sc.lineage_refs.append(SuperchainLineageRecord("lin-01", preserved=True))

    health = verify_corridor_superchain(sc)
    assert not health.is_healthy
    assert health.status == SuperchainStatus.SUPERCHAIN_BROKEN
