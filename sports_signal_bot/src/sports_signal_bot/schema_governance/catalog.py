from .registry import SchemaRegistry
from typing import List

class ContractCatalog:
    def __init__(self, registry: SchemaRegistry):
        self.registry = registry

    def query_contract_family(self, family: str):
        return self.registry.record.schemas.get(family, [])

    def list_all_families(self) -> List[str]:
        return list(self.registry.record.schemas.keys())
