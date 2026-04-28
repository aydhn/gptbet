from sports_signal_bot.approvals.manifests import build_workflow_manifest

def test_workflow_manifest_building():
    man = build_workflow_manifest(
        open_review_items=5,
        approved_count=10,
        rejected_count=2,
        deferred_count=1,
        active_override_count=3,
        unresolved_critical_ack_count=0
    )
    assert man.open_review_items == 5
    assert man.approved_count == 10
    assert man.manifest_id.startswith("wf_")
