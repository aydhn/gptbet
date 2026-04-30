from sports_signal_bot.handoff.council import evaluate_safety_lens, evaluate_governance_lens
from sports_signal_bot.handoff.contracts import CouncilDecisionType

def test_evaluate_safety_lens():
    context = {"risk_level": "high", "rollback_ready": False}
    vote = evaluate_safety_lens(context)
    assert vote.recommendation == CouncilDecisionType.REJECT_HANDOFF
    assert "High risk without rollback procedure." in vote.blockers

def test_evaluate_governance_lens():
    context = {"approvals_complete": False, "docs_linked": True}
    vote = evaluate_governance_lens(context)
    assert vote.recommendation == CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE
    assert "Missing final approvals." in vote.notes
