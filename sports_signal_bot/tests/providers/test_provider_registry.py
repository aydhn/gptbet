from sports_signal_bot.providers.adapters.stub_test_provider import (
    StubTestProviderAdapter,
)
from sports_signal_bot.providers.registry import ProviderRegistry


def test_provider_registry():
    registry = ProviderRegistry()
    adapter = StubTestProviderAdapter("test")
    registry.register("test", adapter)
    assert registry.get("test") == adapter
    assert "test" in registry.list_all()
