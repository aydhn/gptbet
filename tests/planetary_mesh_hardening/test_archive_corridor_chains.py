from src.sports_signal_bot.planetary_mesh_hardening.corridor_chains import build_archive_corridor_chain, verify_archive_corridor_chain
from src.sports_signal_bot.planetary_mesh_hardening.contracts import ChainStatus

def test_intercontinental_handoff_archive_replay():
    # 3) Intercontinental handoff archive replay set
    chain = build_archive_corridor_chain("c_inter", "intercontinental_archive_corridor_chain")
    chain.replay_refs.append("replay_ok")
    verify_archive_corridor_chain(chain)
    assert chain.chain_status == ChainStatus.CHAIN_VERIFIED

def test_archive_corridor_chain_integrity():
    # 4) Archive corridor chain integrity set
    chain = build_archive_corridor_chain("c_int", "archive_restore_corridor_chain")
    chain.replay_refs.append("no_replay")
    verify_archive_corridor_chain(chain)
    assert chain.chain_status == ChainStatus.CHAIN_GAPPED
    assert "Replay support missing" in chain.warnings
