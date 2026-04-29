from sports_signal_bot.providers.normalization import (
    apply_provider_schema_adapter,
    validate_provider_payload_schema,
)


def test_provider_schema_adapter():
    assert validate_provider_payload_schema({}, {}) == True
    assert apply_provider_schema_adapter({"a": 1}, {}) == {"a": 1}
