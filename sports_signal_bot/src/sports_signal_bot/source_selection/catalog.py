from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class SourceCatalogEntry(BaseModel):
    """Definition of a source in the catalog."""
    source_name: str
    source_family: str
    supported_sports: List[str]
    supported_markets: List[str]
    requires_calibration: bool = False
    artifact_paths: Dict[str, str] = Field(default_factory=dict)
    regime_profile_path: Optional[str] = None
    priority: int = 0

class SourceCatalog:
    """Registry of known candidate sources."""
    def __init__(self, entries: Optional[List[SourceCatalogEntry]] = None):
        self.entries = entries or []
        self._lookup = {e.source_name: e for e in self.entries}

    def get_source(self, source_name: str) -> Optional[SourceCatalogEntry]:
        return self._lookup.get(source_name)

    def get_candidates(self, sport: str, market_type: str) -> List[SourceCatalogEntry]:
        """Find sources that technically support the given sport and market."""
        return [
            e for e in self.entries
            if sport in e.supported_sports and market_type in e.supported_markets
        ]
