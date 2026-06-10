from sports_signal_bot.capability_negotiation.contracts import (
    CapabilityDiffRecord,
    NegotiatedTranslationRuleRecord,
    TranslationNeedRecord,
)
from sports_signal_bot.capability_negotiation.translations import (
    evaluate_translation_safety,
    prevent_trust_amplification_via_translation,
)


def test_prevent_trust_amplification():
    translations = [
        NegotiatedTranslationRuleRecord(
            rule_id="safe_mapping",
            source_family="a",
            target_family="b"
        ),
        NegotiatedTranslationRuleRecord(
            rule_id="amplify_trust_mapping",
            source_family="c",
            target_family="d"
        ),
    ]
    safe_translations = prevent_trust_amplification_via_translation(
        translations
    )
    assert len(safe_translations) == 1
    assert safe_translations[0].rule_id == "safe_mapping"


def test_evaluate_translation_safety_safe():
    diff = CapabilityDiffRecord(
        dimensions=[],
        gaps=[],
        translation_needs=[
            TranslationNeedRecord(
                family="a",
                translation_rule="standard map"
            ),
            TranslationNeedRecord(
                family="b",
                translation_rule="safe transform"
            ),
        ],
        narrowing_constraints=[],
    )
    assert evaluate_translation_safety(diff) is True


def test_evaluate_translation_safety_amplification():
    diff = CapabilityDiffRecord(
        dimensions=[],
        gaps=[],
        translation_needs=[
            TranslationNeedRecord(
                family="a",
                translation_rule="standard map"
            ),
            TranslationNeedRecord(
                family="b",
                translation_rule="trust amplification mapping"
            ),
        ],
        narrowing_constraints=[],
    )
    assert evaluate_translation_safety(diff) is False


def test_evaluate_translation_safety_empty():
    diff = CapabilityDiffRecord(
        dimensions=[],
        gaps=[],
        translation_needs=[],
        narrowing_constraints=[]
    )
    assert evaluate_translation_safety(diff) is True


def test_evaluate_translation_safety_case_insensitive():
    diff = CapabilityDiffRecord(
        dimensions=[],
        gaps=[],
        translation_needs=[
            TranslationNeedRecord(
                family="a",
                translation_rule="trust AMPLIFICATION mapping"
            )
        ],
        narrowing_constraints=[],
    )
    assert evaluate_translation_safety(diff) is False

def test_prevent_trust_amplification_empty_list():
    safe_translations = prevent_trust_amplification_via_translation([])
    assert len(safe_translations) == 0


def test_prevent_trust_amplification_all_safe():
    translations = [
        NegotiatedTranslationRuleRecord(
            rule_id="safe_mapping_1",
            source_family="a",
            target_family="b"
        ),
        NegotiatedTranslationRuleRecord(
            rule_id="safe_mapping_2",
            source_family="c",
            target_family="d"
        ),
    ]
    safe_translations = prevent_trust_amplification_via_translation(translations)
    assert len(safe_translations) == 2
    assert safe_translations[0].rule_id == "safe_mapping_1"
    assert safe_translations[1].rule_id == "safe_mapping_2"


def test_prevent_trust_amplification_all_unsafe():
    translations = [
        NegotiatedTranslationRuleRecord(
            rule_id="amplify_trust_mapping_1",
            source_family="a",
            target_family="b"
        ),
        NegotiatedTranslationRuleRecord(
            rule_id="amplify_trust_mapping_2",
            source_family="c",
            target_family="d"
        ),
    ]
    safe_translations = prevent_trust_amplification_via_translation(translations)
    assert len(safe_translations) == 0


def test_prevent_trust_amplification_case_insensitive():
    translations = [
        NegotiatedTranslationRuleRecord(
            rule_id="AMPLIFY_TRUST_mapping",
            source_family="a",
            target_family="b"
        ),
        NegotiatedTranslationRuleRecord(
            rule_id="safe_mapping",
            source_family="c",
            target_family="d"
        ),
    ]
    safe_translations = prevent_trust_amplification_via_translation(translations)
    assert len(safe_translations) == 1
    assert safe_translations[0].rule_id == "safe_mapping"
