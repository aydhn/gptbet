from sports_signal_bot.remediation_copilot import (
    RemediationCopilotSessionManager,
    build_copilot_review_packet,
    build_approval_request,
    evaluate_approval_scope,
    CopilotApprovalRequestParams,
    RehearsalManager,
    compute_execution_readiness,
    build_portable_playbook_bundle,
    adapt_portable_playbook_to_local_policy,
    build_automation_envelope,
    evaluate_self_healing_eligibility,
    PortablePlaybookParams,
    CopilotReviewPacketParams,
    AutomationEnvelopeParams,
)


def test_session_lifecycle():
    manager = RemediationCopilotSessionManager()
    session = manager.create_session("inc_1", ["pb_1", "pb_2"])
    assert session.current_stage == "recommendation_generated"

    updated = manager.update_session_stage(
        session.session_id, "review_packet_prepared"
    )
    assert updated.current_stage == "review_packet_prepared"


def test_review_packet():
    params = CopilotReviewPacketParams(
        session_id="sess_1",
        incident_summary="Summary",
        matched_patterns=["pat_1"],
        confidence_score=0.9,
        selected_playbook_rationale="Rationale",
        scoped_steps=["step_1"],
        required_guards=["guard_1"],
        rehearsal_proposal="proposal",
        rollback_notes="rollback",
        expected_signals=["sig_1"],
        stop_conditions=["stop_1"],
        approval_requirements=["appreq_1"],
    )
    packet = build_copilot_review_packet(params)
    assert packet.confidence_score == 0.9
    assert packet.session_id == "sess_1"


def test_approval():
    params = CopilotApprovalRequestParams(
        packet_ref="rev_1",
        approval_family="step_group_approval",
        scope="isolated",
        max_duration_seconds=3600,
        allowed_step_families=["step_fam_1"],
        forbidden_conditions=["forbid_1"],
        rollback_requirement="req_roll",
        observability_requirement="req_obs",
        review_owner="admin",
    )
    req = build_approval_request(params)
    decision = evaluate_approval_scope(req, "approved", "LGTM")
    assert decision.decision == "approved_for_rehearsal"


def test_rehearsal():
    manager = RehearsalManager()
    ledger = manager.create_ledger("sync_recovery", "sync_lag")
    manager.append_rehearsal_ledger_entry(
        ledger.ledger_id, "rehearsal_started", "Starting rehearsal"
    )
    manager.append_rehearsal_ledger_entry(
        ledger.ledger_id, "rehearsal_completed", "Rehearsal success"
    )

    assert len(ledger.entries) == 2


def test_execution_readiness():
    ready = compute_execution_readiness(
        "sess_1", True, True, True, True, True, True, True, True, True, True
    )
    assert ready.status == "staged_execution_preparation_ready"
    assert len(ready.blockers) == 0

    blocked = compute_execution_readiness(
        "sess_1", False, True, False, True, True, True, True, True, True, True
    )
    assert blocked.status == "blocked"
    assert "approval_incomplete" in blocked.blockers


def test_federation_and_adaptation():
    params = PortablePlaybookParams(
        family="sync",
        step_taxonomy=["step_1"],
        scope_constraints=["scope_1"],
        required_guards=[],
        required_approvals=[],
        rehearsal_requirements=[],
        rollback_notes="rollback",
        observability_expectations=[],
        known_safe_subset_notes="safe subset",
        nonportable_step_markers=[],
        confidence_notes="confidence",
    )
    bundle = build_portable_playbook_bundle(params)

    adapt_clean = adapt_portable_playbook_to_local_policy(bundle, [])
    assert adapt_clean.outcome == "adapted_clean"

    adapt_restricted = adapt_portable_playbook_to_local_policy(
        bundle, ["unsafe_semantic_widening"]
    )
    assert adapt_restricted.outcome == "quarantined_for_manual_mapping"


def test_automation_prep():
    params = AutomationEnvelopeParams(
        allowed_step_families=["step_1"],
        maximum_scope="isolated",
        required_guards=[],
        required_approvals_retained=[],
        required_rehearsal_evidence=[],
        required_rollback_guarantees=[],
        forbidden_incident_families=[],
        observability_minimums=[],
        stop_conditions=[],
    )
    env = build_automation_envelope(params)
    assert env.allowed_step_families == ["step_1"]

    eligibility = evaluate_self_healing_eligibility("sess_1", True, True, True)
    assert eligibility.eligibility_status == "bounded_candidate"

    blocked = evaluate_self_healing_eligibility("sess_1", False, True, True)
    assert blocked.eligibility_status == "blocked_for_automation"
