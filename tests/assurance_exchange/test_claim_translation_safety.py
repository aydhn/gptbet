from sports_signal_bot.assurance_exchange.translations import translate_assurance_claim, validate_translation_safety
from sports_signal_bot.assurance.contracts import ClaimFamily

def test_validate_translation_safety():
    t = translate_assurance_claim(
        translation_id="t_1",
        source_claim_family=ClaimFamily.e2e_promotion_claim,
        destination_claim_family=ClaimFamily.e2e_promotion_claim,
        mapping_type="direct",
        semantic_loss_risk="high",
        strengthened_or_weakened="weakened",
        added_caveats=[],
        required_verification_steps=[],
        accepted_profiles=[]
    )
    assert validate_translation_safety(t) is False

    t.added_caveats.append("Caveat applied")
    assert validate_translation_safety(t) is True
