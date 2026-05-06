from src.sports_signal_bot.geo_quorum_hardening.evacuation_chains import build_rolling_evacuation_audit_chain

def test_build_rolling_evacuation_audit_chain_healthy():
    inputs = {
        "explicit_wave_scope": True,
        "broken_dependency": False,
        "no_safe_continuity_preserved": True
    }
    record = build_rolling_evacuation_audit_chain(inputs)
    assert record.chain_status == "chain_verified"

def test_build_rolling_evacuation_audit_chain_broken():
    inputs = {
        "explicit_wave_scope": True,
        "broken_dependency": True,
        "no_safe_continuity_preserved": True
    }
    record = build_rolling_evacuation_audit_chain(inputs)
    assert record.chain_status == "chain_broken"
