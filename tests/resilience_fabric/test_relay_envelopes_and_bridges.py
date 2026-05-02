import pytest
from src.sports_signal_bot.resilience_fabric.contracts import ExternalEventRelayRecord, DeliveryMode
from src.sports_signal_bot.resilience_fabric.relays import build_relay_envelope, verify_relay_envelope, decide_relay_lane

def test_relay_envelope_verification():
    envelope = build_relay_envelope(
        relay_id="relay_1",
        event_family="external_catalog_relay",
        source_identity="source_a",
        payload={"data": "test_value"}
    )

    assert verify_relay_envelope(envelope) is True

    # Tamper with payload
    envelope.payload["data"] = "tampered"
    assert verify_relay_envelope(envelope) is False

def test_decide_relay_lane_quarantine():
    relay = ExternalEventRelayRecord(
        relay_id="relay_1",
        relay_family="external_catalog_relay",
        source_ref="test",
        supported_event_families=["test"],
        delivery_mode=DeliveryMode.review_quarantine_bridge,
        integrity_mode="strict",
        freshness_expectation="PT1H",
        review_policy="review_quarantine_bridge",
        active_status="active",
        warnings=[]
    )

    envelope = build_relay_envelope(
        relay_id="relay_1",
        event_family="external_catalog_relay",
        source_identity="source_a",
        payload={"data": "test_value"}
    )

    assert decide_relay_lane(envelope, relay) == "quarantine"

def test_decide_relay_lane_verified():
    relay = ExternalEventRelayRecord(
        relay_id="relay_1",
        relay_family="external_catalog_relay",
        source_ref="test",
        supported_event_families=["test"],
        delivery_mode=DeliveryMode.event_batch_bridge,
        integrity_mode="strict",
        freshness_expectation="PT1H",
        review_policy="auto_accept",
        active_status="active",
        warnings=[]
    )

    envelope = build_relay_envelope(
        relay_id="relay_1",
        event_family="external_catalog_relay",
        source_identity="source_a",
        payload={"data": "test_value"}
    )

    assert decide_relay_lane(envelope, relay) == "verified_signal"
