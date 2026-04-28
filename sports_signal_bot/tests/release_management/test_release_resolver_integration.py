from sports_signal_bot.inference.resolver import ArtifactResolver
from sports_signal_bot.release_management.state import ChannelStateManager

def test_resolver_respects_freeze_and_quarantine():
    manager = ChannelStateManager(data_dir="tests/test_data_res_integ")

    # quarantine a stable base id
    manager.mark_artifact_quarantined("football", "1x2", "mod_football_1x2_stable_v1.0")

    resolver = ArtifactResolver(state_manager=manager)

    chain = resolver.resolve_chain("football", "1x2", policy="latest_stable")

    assert chain.model_artifact_id is None
    assert "Artifact is quarantined." in chain.warnings

    manager.freeze_channel("basketball", "moneyline", "test freeze fallback")

    chain2 = resolver.resolve_chain("basketball", "moneyline", policy="latest_compatible")
    # since it's frozen, should fall back to stable.
    assert "Channel is currently frozen." in chain2.warnings
