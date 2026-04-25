import json
from pathlib import Path
from typing import Any, Dict, List


class DataReader:
    @staticmethod
    def read_json(file_path: Path) -> List[Dict[str, Any]]:
        if not file_path.exists():
            return []
        with open(file_path, "r") as f:
            return json.load(f)
