import pytest
from sports_signal_bot.remediation_copilot import (
    RemediationCopilotSessionManager,
    build_copilot_review_packet,
    build_approval_request,
    evaluate_approval_scope,
    RehearsalManager,
    compute_execution_readiness,
    build_portable_playbook_bundle,
    adapt_portable_playbook_to_local_policy,
    build_automation_envelope,
    evaluate_self_healing_eligibility
)

def test_session_lifecycle():
    manager = RemediationCopilotSessionManager()
    session = manager.create_session("inc_1", ["pb_1", "pb_2"])
    assert session.current_stage == "recommendation_generated"

    updated = manager.update_session_stage(session.session_id, "review_packet_prepared")
    assert updated.current_stage == "review_packet_prepared"

def test_review_packet():
    packet = build_copilot_review_packet(
        "sess_1", "Summary", ["pat_1"], 0.9, "Rationale", ["step_1"], ["guard_1"], "proposal", "rollback", ["sig_1"], ["stop_1"], ["appreq_1"]
    )
    assert packet.confidence_score == 0.9
    assert packet.session_id == "sess_1"

def test_approval():
    req = build_approval_request("rev_1", "step_group_approval", "isolated", 3600, ["step_fam_1"], ["forbid_1"], "req_roll", "req_obs", "admin")
    decision = evaluate_approval_scope(req, "approved", "LGTM")
    assert decision.decision == "approved_for_rehearsal"

def test_rehearsal():
    manager = RehearsalManager()
    ledger = manager.create_ledger("sync_recovery", "sync_lag")
    manager.append_rehearsal_ledger_entry(ledger.ledger_id, "rehearsal_started", "Starting rehearsal")
    manager.append_rehearsal_ledger_entry(ledger.ledger_id, "rehearsal_completed", "Rehearsal success")

    assert len(ledger.entries) == 2

def test_execution_readiness():
    ready = compute_execution_readiness("sess_1", True, True, True, True, True, True, True, True, True, True)
    assert ready.status == "staged_execution_preparation_ready"
    assert len(ready.blockers) == 0

    blocked = compute_execution_readiness("sess_1", False, True, False, True, True, True, True, True, True, True)
    assert blocked.status == "blocked"
    assert "approval_incomplete" in blocked.blockers

def test_federation_and_adaptation():
    bundle = build_portable_playbook_bundle("sync", ["step_1"], ["scope_1"], [], [], [], "rollback", [], "safe subset", [], "confidence")

    adapt_clean = adapt_portable_playbook_to_local_policy(bundle, [])
    assert adapt_clean.outcome == "adapted_clean"

    adapt_restricted = adapt_portable_playbook_to_local_policy(bundle, ["unsafe_semantic_widening"])
    assert adapt_restricted.outcome == "quarantined_for_manual_mapping"

def test_automation_prep():
    env = build_automation_envelope(["step_1"], "isolated", [], [], [], [], [], [], [])
    assert env.allowed_step_families == ["step_1"]

    eligibility = evaluate_self_healing_eligibility("sess_1", True, True, True)
    assert eligibility.eligibility_status == "bounded_candidate"

    blocked = evaluate_self_healing_eligibility("sess_1", False, True, True)
    assert blocked.eligibility_status == "blocked_for_automation"
