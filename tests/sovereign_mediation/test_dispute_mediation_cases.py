from sports_signal_bot.sovereign_mediation.disputes import open_sovereign_audit_dispute, run_dispute_mediation
from sports_signal_bot.sovereign_mediation.contracts import DisputeCaseRecord

def test_dispute_mediation():
    dispute = open_sovereign_audit_dispute("test_family", "proj_1", ["proj_2"])
    case = DisputeCaseRecord(
        dispute_case_id="dc_1",
        dispute_ref=dispute.dispute_id,
        case_family="audit",
        input_claim_refs=[],
        input_evidence_refs=["ev_1"],
        replay_requirement="match",
        sovereignty_constraints="sovereignty_deny",
        mediation_needed=True,
        case_status="open"
    )

    outcome = run_dispute_mediation(dispute, case)
    assert outcome == "preserve_local_deny"
