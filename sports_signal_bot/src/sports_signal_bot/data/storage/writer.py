from pathlib import Path
import json
import pandas as pd
from typing import List, Dict, Any
from pydantic import BaseModel
import os

class DataWriter:
    @staticmethod
    def write_json(data: List[Dict[str, Any]], path: Path, filename: str) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / filename
        with open(file_path, 'w') as f:
             json.dump(data, f, indent=2, default=str)
        return file_path

    @staticmethod
    def write_manifest(manifest: BaseModel, path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{manifest.ingest_id}_manifest.json" # type: ignore
        with open(file_path, 'w') as f:
            f.write(manifest.model_dump_json(indent=2))
        return file_path
