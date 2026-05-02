from typing import List, Dict, Any
from src.sports_signal_bot.capability_negotiation.contracts import (
    NegotiatedTranslationRuleRecord,
    CapabilityDiffRecord
)

def evaluate_translation_safety(diff: CapabilityDiffRecord) -> bool:
    """
    Evaluates if the required translations are safe.
    Foreign claim translation cannot increase trust.
    """
    for need in diff.translation_needs:
        if "amplification" in need.translation_rule.lower():
            return False
    return True

def prevent_trust_amplification_via_translation(translations: List[NegotiatedTranslationRuleRecord]) -> List[NegotiatedTranslationRuleRecord]:
    """
    Filters out any translation rules that would artificially amplify trust.
    """
    safe_translations = []
    for t in translations:
        # Placeholder for complex trust evaluation logic.
        # In this phase, we assume rules not containing 'amplify_trust' are safe.
        if "amplify_trust" not in t.rule_id.lower():
             safe_translations.append(t)
    return safe_translations
