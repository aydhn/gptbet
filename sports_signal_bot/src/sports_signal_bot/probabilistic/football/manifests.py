import json
from pathlib import Path
from typing import List

from sports_signal_bot.probabilistic.football.contracts import \
    FootballProbabilityRecord


def write_prediction_manifest(
    records: List[FootballProbabilityRecord], out_dir: Path, filename: str
):
    """Writes standardized probability records to a JSON lines file."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename

    with open(out_path, "w") as f:
        for r in records:
            # We use model_dump_json to handle datetime serialization
            f.write(r.model_dump_json() + "\n")

    return out_path
