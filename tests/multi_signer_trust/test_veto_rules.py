from datetime import datetime
from sports_signal_bot.multi_signer_trust.thresholds import evaluate_veto_rules
from sports_signal_bot.multi_signer_trust.contracts import VetoRuleRecord, VetoDecisionRecord

def test_veto_rules():
    policy_veto = VetoRuleRecord(veto_enabled_groups=["g1"])
    veto = VetoDecisionRecord(signer_id="u1", group_name="g1", reason="block", timestamp=datetime.utcnow())

    assert evaluate_veto_rules([veto], policy_veto) == True

    veto2 = VetoDecisionRecord(signer_id="u2", group_name="g2", reason="block", timestamp=datetime.utcnow())
    assert evaluate_veto_rules([veto2], policy_veto) == False
