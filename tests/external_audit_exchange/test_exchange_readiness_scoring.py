import pytest
from sports_signal_bot.external_audit_exchange.readiness import generate_exchange_readiness_record

def test_generate_exchange_readiness_record():
    metrics = {
        "packet_completeness": 90.0,
        "responder_diversity": 80.0,
        "notarization_coverage": 100.0
    }
    record = generate_exchange_readiness_record(metrics)
    assert record.score > 80.0
    assert record.status == "advanced_public_style_readiness"
