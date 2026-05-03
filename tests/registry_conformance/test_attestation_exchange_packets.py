from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.exchanges import (
    build_attestation_exchange_packet,
    validate_attestation_for_exchange,
)


def test_exchange_packet_validation():
    now = datetime.now(timezone.utc)
    packet = build_attestation_exchange_packet(
        source_registry_ref="r1",
        attestation_refs=["a1"],
        corridor_refs=["c1"],
        treaty_refs=["t1"],
        scope="review_only",
        valid_until=now + timedelta(days=1),
    )
    decision = validate_attestation_for_exchange(packet)
    assert decision.decision == "validated"

    packet.validity_window.valid_until = now - timedelta(days=1)
    decision = validate_attestation_for_exchange(packet)
    assert decision.decision == "blocked"
