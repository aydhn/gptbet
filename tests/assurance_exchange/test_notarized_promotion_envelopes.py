from sports_signal_bot.assurance_exchange.notarized_envelopes import build_notarized_promotion_envelope, verify_notarized_envelope

def test_verify_notarized_envelope():
    env = build_notarized_promotion_envelope(
        notarized_envelope_id="env_1",
        promotion_envelope_ref="p_1",
        digest_ref="d_1",
        notarization_ref="n_1",
        publication_scope="local",
        exchange_visibility_profile="private"
    )
    assert verify_notarized_envelope(env) is True
