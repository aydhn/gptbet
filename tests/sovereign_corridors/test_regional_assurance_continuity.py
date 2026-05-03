from sports_signal_bot.sovereign_corridors.continuity import build_continuity_session, evaluate_assurance_continuity, detect_continuity_gaps

def test_continuity():
    session = build_continuity_session("s1")
    assert session.status == "monitoring"

    assert evaluate_assurance_continuity({"has_gaps": True}) == "continuity_blocked"
    assert evaluate_assurance_continuity({"has_gaps": False}) == "continuity_verified"

    gaps = detect_continuity_gaps({"translation_complete": False})
    assert len(gaps) == 1
    assert gaps[0].severity == "high"
