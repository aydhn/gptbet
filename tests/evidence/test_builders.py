from sports_signal_bot.evidence.builders.decision import DecisionEvidenceBuilder
from sports_signal_bot.evidence.builders.why_not import WhyNotEvidenceBuilder
from sports_signal_bot.evidence.claims import build_claim

def test_decision_evidence_builder():
    builder = DecisionEvidenceBuilder("tgt_1", "operator")
    claim = build_claim("c1", "test", "test claim", "high", 0.9)
    builder.add_claim(claim)
    bundle = builder.build()
    assert bundle.bundle_type == "decision_evidence"
    assert bundle.target_entity_id == "tgt_1"
    assert len(bundle.claims) == 1
    assert bundle.confidence_band == "high"

def test_why_not_evidence_builder():
    builder = WhyNotEvidenceBuilder("tgt_2", "reviewer")
    claim = build_claim("c2", "test", "test claim", "disputed", 0.1)
    builder.add_claim(claim)
    bundle = builder.build()
    assert bundle.bundle_type == "why_not_evidence"
    assert bundle.confidence_band == "disputed"
