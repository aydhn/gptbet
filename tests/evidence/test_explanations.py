from sports_signal_bot.evidence.builders.decision import DecisionEvidenceBuilder
from sports_signal_bot.evidence.claims import build_claim
from sports_signal_bot.evidence.explanations import explain_why_decision, explain_why_not

def test_explain_why_decision():
    builder = DecisionEvidenceBuilder("tgt_1", "operator")
    claim = build_claim("c1", "test", "Reason A", "high", 0.9)
    builder.add_claim(claim)
    bundle = builder.build()

    explanation = explain_why_decision(bundle, "summary")
    assert "Reason A" in explanation

def test_explain_why_not():
    builder = DecisionEvidenceBuilder("tgt_1", "operator")
    bundle = builder.build()

    explanation = explain_why_not(bundle, ["Reason B"])
    assert "Reason B" in explanation
