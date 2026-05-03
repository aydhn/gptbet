from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.exchanges import (
    build_attestation_exchange_packet,
)
from sports_signal_bot.registry_conformance.exchange_validity import (
    watch_attestation_exchange_validity,
)
from sports_signal_bot.registry_conformance.contracts import ExchangeCaveatRecord


def test_watch_exchange_validity():
    now = datetime.now(timezone.utc)
    packet = build_attestation_exchange_packet(
        source_registry_ref="r1",
        attestation_refs=["a1"],
        corridor_refs=[],
        treaty_refs=[],
        scope="visibility_only",
        valid_until=now + timedelta(days=1),
    )
    packet.exchange_status = "validated"

    status, reasons = watch_attestation_exchange_validity(packet)
    assert status == "exchange_remains_valid"

    packet.caveat_refs.append(
        ExchangeCaveatRecord(caveat_code="C1", description="Caveat")
    )
    status, reasons = watch_attestation_exchange_validity(packet)
    assert status == "exchange_caveated"
