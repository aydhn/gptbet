import json
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Union

def save_artifact(data: Union[BaseModel, dict, list], filename: str, output_dir: str = "results") -> None:
    """Saves a Pydantic model or dict/list as a JSON artifact."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_dir) / filename

    with open(filepath, "w") as f:
        if isinstance(data, BaseModel):
            f.write(data.model_dump_json(indent=2))
        else:
            json.dump(data, f, indent=2, default=str)
