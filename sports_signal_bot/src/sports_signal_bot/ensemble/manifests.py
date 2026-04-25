import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EnsembleRunManifest(BaseModel):
    run_id: str
    sport: str
    market_type: str
    ensemble_strategy: str
    target_classes: List[str]
    config: Dict[str, Any]
    source_summary: Dict[str, int] = Field(default_factory=dict)
    run_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    status: str = "success"
    warnings: List[str] = Field(default_factory=list)
    output_path: Optional[str] = None

    def save(self, filepath: str):
        with open(filepath, "w") as f:
            f.write(self.json(indent=2))
