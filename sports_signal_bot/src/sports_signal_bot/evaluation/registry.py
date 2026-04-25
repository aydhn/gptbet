from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


class EvaluationRegistry:
    """Registry to manage discovered and registered evaluation sources (models, benchmarks)."""

    def __init__(self):
        self.sources: Dict[str, Dict[str, Any]] = {}

    def register_source(
        self,
        name: str,
        family: str,
        artifact_path: Path,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Registers a prediction source to be evaluated."""
        self.sources[name] = {
            "family": family,
            "path": artifact_path,
            "metadata": metadata or {},
        }

    def get_registered_sources(self) -> List[str]:
        return list(self.sources.keys())

    def get_source_paths(self, names: Optional[List[str]] = None) -> List[Path]:
        """Gets artifact paths for specified sources, or all if none specified."""
        if names is None:
            names = self.get_registered_sources()

        paths = []
        for name in names:
            if name in self.sources:
                paths.append(self.sources[name]["path"])
        return paths
