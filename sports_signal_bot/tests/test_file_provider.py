import pytest

from sports_signal_bot.core.constants import SportType
from sports_signal_bot.data.providers.file_provider import FileFixtureProvider


def test_file_fixture_provider_config():
    config = {
        "name": "test_provider",
        "football": {"fixtures_path": "path/to/fixtures.csv"},
    }
    provider = FileFixtureProvider(config)
    assert provider.provider_name == "test_provider"
    assert SportType.FOOTBALL in provider.sport_support()
    assert SportType.BASKETBALL not in provider.sport_support()
