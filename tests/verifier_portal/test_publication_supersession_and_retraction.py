from sports_signal_bot.verifier_portal.publication import mark_publication_superseded, build_retraction_notice, summarize_publication_lifecycle

def test_mark_publication_superseded():
    res = mark_publication_superseded("pub1")
    assert res.superseded

def test_build_retraction_notice():
    notice = build_retraction_notice("pub1", "test reason")
    assert notice.tombstone_id == "tombstone_pub1"

def test_summarize_publication_lifecycle():
    summary = summarize_publication_lifecycle("pub1", ["current", "superseded"])
    assert summary["current_state"] == "superseded"
    assert len(summary["lifecycle_states"]) == 2
