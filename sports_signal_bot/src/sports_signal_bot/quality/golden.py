import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from sports_signal_bot.quality.contracts import GoldenOutputRecord
from sports_signal_bot.quality.utils import normalize_dynamic_fields

class GoldenRegistry:
    def __init__(self, base_path: str = "sports_signal_bot/tests/quality/golden_data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_path(self, output_id: str) -> Path:
        return self.base_path / f"{output_id}.json"

    def load_golden_output(self, output_id: str) -> Optional[GoldenOutputRecord]:
        path = self._get_path(output_id)
        if not path.exists():
            return None
        with open(path, "r") as f:
            data = json.load(f)
            return GoldenOutputRecord(**data)

    def update_golden_with_explicit_flag(self, output_id: str, data: Any, version: str = "1.0", explicit_flag: bool = False):
        if not explicit_flag:
            raise ValueError(f"Explicit flag required to update golden output {output_id}")

        record = GoldenOutputRecord(
            output_id=output_id,
            version=version,
            timestamp="2024-01-01T00:00:00Z", # placeholder
            data=data
        )
        with open(self._get_path(output_id), "w") as f:
            f.write(record.model_dump_json(indent=2))

    def compare_to_golden(self, output_id: str, actual_data: Any, dynamic_keys: List[str] = None) -> bool:
        golden = self.load_golden_output(output_id)
        if not golden:
            print(f"Warning: Missing golden baseline for {output_id}")
            return False

        dynamic_keys = dynamic_keys or ["timestamp", "run_id", "path"]

        normalized_actual = normalize_dynamic_fields(actual_data, dynamic_keys)
        normalized_golden = normalize_dynamic_fields(golden.data, dynamic_keys)

        # In a real system, we'd use a diffing library and return a detailed report
        return normalized_actual == normalized_golden

    def summarize_golden_diffs(self, output_id: str, actual_data: Any, dynamic_keys: List[str] = None) -> Dict[str, Any]:
        golden = self.load_golden_output(output_id)
        if not golden:
            return {"status": "missing_baseline"}

        dynamic_keys = dynamic_keys or ["timestamp", "run_id", "path"]
        normalized_actual = normalize_dynamic_fields(actual_data, dynamic_keys)
        normalized_golden = normalize_dynamic_fields(golden.data, dynamic_keys)

        is_match = normalized_actual == normalized_golden
        return {
            "status": "match" if is_match else "diff",
            "diff_count": 0 if is_match else 1 # simplified
        }
