import pytest
from sports_signal_bot.schema_governance.adapters import VersionedLoader, ContractAdapter, ManifestShim
from sports_signal_bot.schema_governance.registry import SchemaRegistry

def test_loader_with_legacy_version():
    registry = SchemaRegistry()
    adapter = ContractAdapter()
    loader = VersionedLoader(registry, adapter)

    legacy_data = {"data": "value"} # missing schema_version
    loaded = loader.load(legacy_data, "test_family")

    assert "schema_version" in loaded
    assert loaded["schema_version"] == "v0.0.0"
