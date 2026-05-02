from typing import List, Dict, Any
from .contracts import ClaimTranslationRecord
from sports_signal_bot.assurance.contracts import ClaimFamily

def translate_assurance_claim(
    translation_id: str,
    source_claim_family: ClaimFamily,
    destination_claim_family: ClaimFamily,
    mapping_type: str,
    semantic_loss_risk: str,
    strengthened_or_weakened: str,
    added_caveats: List[str],
    required_verification_steps: List[str],
    accepted_profiles: List[str]
) -> ClaimTranslationRecord:
    """Translates an assurance claim based on mapping rules."""
    return ClaimTranslationRecord(
        translation_id=translation_id,
        source_claim_family=source_claim_family,
        destination_claim_family=destination_claim_family,
        mapping_type=mapping_type,
        semantic_loss_risk=semantic_loss_risk,
        strengthened_or_weakened=strengthened_or_weakened,
        added_caveats=added_caveats,
        required_verification_steps=required_verification_steps,
        accepted_profiles=accepted_profiles
    )

def validate_translation_safety(translation: ClaimTranslationRecord) -> bool:
    """Validates the safety of a claim translation."""
    if translation.semantic_loss_risk in ["high", "critical"] and not translation.added_caveats:
        return False
    return True

def attach_translation_caveats(translation: ClaimTranslationRecord, caveats: List[str]) -> ClaimTranslationRecord:
    translation.added_caveats.extend(caveats)
    return translation

def reject_semantically_unsafe_translation(translation: ClaimTranslationRecord) -> bool:
    """Returns True if the translation is deemed unsafe and should be rejected."""
    if translation.mapping_type == "nonportable_reject":
        return True
    return False

def summarize_claim_translation_risk(translations: List[ClaimTranslationRecord]) -> Dict[str, Any]:
    high_risk = sum(1 for t in translations if t.semantic_loss_risk in ["high", "critical"])
    return {
        "total_translations": len(translations),
        "high_risk_translations": high_risk
    }

def map_claim_family_between_registries(source_family: ClaimFamily, mapping_rules: List[ClaimTranslationRecord]) -> ClaimFamily:
    for rule in mapping_rules:
        if rule.source_claim_family == source_family:
            return rule.destination_claim_family
    return source_family # default to same if no rule

def classify_claim_interoperability(source_family: ClaimFamily, dest_family: ClaimFamily) -> str:
    if source_family == dest_family:
        return "fully_interoperable"
    return "interoperable_with_translation"

def determine_claim_portability(claim_family: ClaimFamily) -> str:
    # default all are portable for now
    return "portable"

def verify_translation_output(translation: ClaimTranslationRecord) -> bool:
    return validate_translation_safety(translation)
