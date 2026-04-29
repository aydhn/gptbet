from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .versions import SchemaVersionRecord
from .contracts import ContractDefinitionRecord
from .compatibility import CompatibilityResultRecord, check_backward_compatibility, check_forward_compatibility

class SchemaRegistryRecord(BaseModel):
    schemas: Dict[str, List[ContractDefinitionRecord]] = {}

class SchemaRegistry:
    def __init__(self):
        self.record = SchemaRegistryRecord()

    def register_schema(self, contract: ContractDefinitionRecord):
        family = contract.manifest_family
        if family not in self.record.schemas:
            self.record.schemas[family] = []
        self.record.schemas[family].append(contract)

    def list_known_versions(self, family: str) -> List[str]:
        if family not in self.record.schemas:
            return []
        return [c.version.version_string for c in self.record.schemas[family]]

    def resolve_latest_version(self, family: str) -> Optional[ContractDefinitionRecord]:
        if family not in self.record.schemas or not self.record.schemas[family]:
            return None
        return self.record.schemas[family][-1]

    def resolve_version(self, family: str, version_str: str) -> Optional[ContractDefinitionRecord]:
        if family not in self.record.schemas:
            return None
        for c in self.record.schemas[family]:
            if c.version.version_string == version_str:
                return c
        return None

class VersionResolver:
    def __init__(self, registry: SchemaRegistry):
        self.registry = registry

    def resolve(self, family: str, version_str: str) -> Optional[ContractDefinitionRecord]:
        return self.registry.resolve_version(family, version_str)
