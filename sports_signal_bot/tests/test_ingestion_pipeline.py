import pytest

from sports_signal_bot.core.constants import SportType
from sports_signal_bot.data.ingestion.orchestrator import IngestionOrchestrator
from sports_signal_bot.data.providers.mock_provider import (
    AdvancedMockFixtureProvider,
    AdvancedMockOddsProvider,
    AdvancedMockStatsProvider,
)


def test_ingestion_orchestrator_mock():
    config = {"name": "test_mock", "football": {"enabled": True}}
    fixture_prov = AdvancedMockFixtureProvider(config)
    orchestrator = IngestionOrchestrator()

    # We'll just verify it runs and generates a manifest without errors
    manifest = orchestrator.ingest_fixtures(fixture_prov, SportType.FOOTBALL)

    assert manifest is not None
    assert manifest.provider == "test_mock"
    assert manifest.dataset_type == "fixtures"
    assert manifest.record_count > 0
    assert manifest.valid_count > 0
