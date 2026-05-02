from src.sports_signal_bot.capability_negotiation.contracts import NegotiatedTranslationRuleRecord
from src.sports_signal_bot.capability_negotiation.translations import prevent_trust_amplification_via_translation

def test_prevent_trust_amplification():
    translations = [
        NegotiatedTranslationRuleRecord(rule_id="safe_mapping", source_family="a", target_family="b"),
        NegotiatedTranslationRuleRecord(rule_id="amplify_trust_mapping", source_family="c", target_family="d")
    ]
    safe_translations = prevent_trust_amplification_via_translation(translations)
    assert len(safe_translations) == 1
    assert safe_translations[0].rule_id == "safe_mapping"
