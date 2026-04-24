import pytest
from sports_signal_bot.features.registry import FeatureRegistry
from sports_signal_bot.features.builders.context import ContextFeatureBuilder
from sports_signal_bot.features.builders.football_strength import FootballTeamStrengthBuilder

def test_registry_registration():
    registry = FeatureRegistry()
    registry.register(ContextFeatureBuilder())

    assert len(registry.list_builders()) == 1
    assert registry.get_builder("context_features") is not None

def test_registry_sport_filtering():
    registry = FeatureRegistry()
    registry.register(ContextFeatureBuilder()) # all
    registry.register(FootballTeamStrengthBuilder()) # football

    assert len(registry.list_builders(sport="football")) == 2
    assert len(registry.list_builders(sport="basketball")) == 1

def test_registry_family_filtering():
    registry = FeatureRegistry()
    registry.register(ContextFeatureBuilder()) # identity_context

    assert len(registry.select_by_family("identity_context")) == 1
    assert len(registry.select_by_family("non_existent")) == 0
