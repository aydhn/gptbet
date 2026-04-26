from sports_signal_bot.inference.resolver import ArtifactResolver


def test_artifact_chain_resolution():
    resolver = ArtifactResolver()

    # Normal case
    chain1 = resolver.resolve_chain("football", "1x2", "latest_compatible")
    assert chain1.is_valid is True
    assert "1x2" in chain1.model_artifact_id
    assert chain1.stacker_artifact_id is not None

    # Degrade/Fallback case
    chain2 = resolver.resolve_chain("basketball", "moneyline", "latest_compatible")
    # Our mock simulates stacker missing for moneyline
    assert chain2.is_valid is True
    assert chain2.stacker_artifact_id is None
