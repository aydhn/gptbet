from sports_signal_bot.handoff.supersession import compare_handoff_candidates, resolve_handoff_supersession

def test_compare_handoff_candidates():
    c1 = {"candidate_release_id": "c1", "readiness_score": 0.9}
    c2 = {"candidate_release_id": "c2", "readiness_score": 0.8}
    assert compare_handoff_candidates(c1, c2) == "c1"

def test_resolve_handoff_supersession():
    c1 = {"candidate_release_id": "c1", "target_component_family": "f1", "readiness_score": 0.9}
    c2 = {"candidate_release_id": "c2", "target_component_family": "f1", "readiness_score": 0.8}
    candidates = resolve_handoff_supersession([c1, c2])

    c1_resolved = next(c for c in candidates if c["candidate_release_id"] == "c1")
    c2_resolved = next(c for c in candidates if c["candidate_release_id"] == "c2")

    assert not c1_resolved.get("is_superseded")
    assert c2_resolved.get("is_superseded")
    assert c2_resolved.get("superseded_by") == "c1"
