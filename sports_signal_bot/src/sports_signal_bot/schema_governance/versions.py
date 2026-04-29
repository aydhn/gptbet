from enum import Enum
from pydantic import BaseModel, Field

class CompatibilityPolicy(str, Enum):
    STRICT = "strict"
    FLEXIBLE = "flexible"

class SchemaVersionRecord(BaseModel):
    schema_name: str
    major_version: int
    minor_version: int
    patch_version: int
    schema_version: str = Field(..., description="String representation e.g. v1.0.0")
    compatibility_policy: CompatibilityPolicy = CompatibilityPolicy.STRICT
    breaking_change_flag: bool = False

    @property
    def version_string(self) -> str:
        return f"v{self.major_version}.{self.minor_version}.{self.patch_version}"

    def __str__(self):
        return self.version_string
