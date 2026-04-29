from sports_signal_bot.providers.contracts import DataFamily
from sports_signal_bot.providers.requests import ProviderRequestRecord
from sports_signal_bot.providers.routing import CachedFirstForPreviewStrategy


def test_cached_fallback_behavior():
    strategy = CachedFirstForPreviewStrategy()
    req = ProviderRequestRecord(sport="football", data_family=DataFamily.FIXTURES)
    providers = [
        {
            "provider_name": "remote",
            "provider_kind": "remote_json_api",
            "data_family": DataFamily.FIXTURES,
        },
        {
            "provider_name": "cache",
            "provider_kind": "cached_proxy",
            "data_family": DataFamily.FIXTURES,
        },
    ]
    res = strategy.select_providers(req, providers)
    assert res[0] == "cache"
