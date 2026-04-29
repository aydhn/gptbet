import pytest
from sports_signal_bot.schema_governance.registry import SchemaRegistry
from sports_signal_bot.schema_governance.versions import SchemaVersionRecord
from sports_signal_bot.schema_governance.contracts import ContractDefinitionRecord

def test_schema_registry_registration():
    registry = SchemaRegistry()
    version = SchemaVersionRecord(
        schema_name="inference",
        major_version=1, minor_version=0, patch_version=0,
        schema_version="v1.0.0"
    )
    contract = ContractDefinitionRecord(
        version=version,
        manifest_family="inference_manifest",
        contract_family="inference_contract"
    )

    registry.register_schema(contract)
    assert len(registry.list_known_versions("inference_manifest")) == 1
    assert registry.resolve_latest_version("inference_manifest") == contract
