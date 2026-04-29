from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .versions import SchemaVersionRecord

class ContractDefinitionRecord(BaseModel):
    version: SchemaVersionRecord
    required_fields: List[str] = Field(default_factory=list)
    optional_fields: List[str] = Field(default_factory=list)
    deprecated_fields: List[str] = Field(default_factory=list)
    extension_fields: Dict[str, Any] = Field(default_factory=dict)
    migration_path: Optional[str] = None
    manifest_family: str
    contract_family: str
