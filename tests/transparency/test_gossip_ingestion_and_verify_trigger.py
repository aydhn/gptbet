import pytest
from sports_signal_bot.transparency.gossip import GossipManager
from sports_signal_bot.transparency.contracts import GossipTopic, VerificationStatus

def test_gossip_ingestion():
    mgr = GossipManager()

    env = mgr.build_gossip_envelope(
        topic=GossipTopic.SIGNED_CHECKPOINT_UPDATES,
        source_plane="plane_x",
        details={"cp_id": "cp_123"},
        signature="valid_sig"
    )

    is_valid = mgr.ingest_gossip_signal(env)
    assert is_valid == True

    bad_env = mgr.build_gossip_envelope(
        topic=GossipTopic.SIGNED_CHECKPOINT_UPDATES,
        source_plane="plane_y",
        details={"cp_id": "cp_456"},
        signature=""
    )

    with pytest.raises(ValueError):
        mgr.ingest_gossip_signal(bad_env)
