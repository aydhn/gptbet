import json
import logging
from pathlib import Path
from .contracts import TelegramDispatchManifest

logger = logging.getLogger(__name__)

class ManifestWriter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_manifest(self, manifest: TelegramDispatchManifest) -> Path:
        file_path = self.base_dir / f"dispatch_manifest_{manifest.run_id}.json"

        # Pydantic v1 vs v2 compatibility check
        try:
            data = manifest.model_dump(mode="json")
        except AttributeError:
             data = json.loads(manifest.json())

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Wrote dispatch manifest to {file_path}")
        return file_path
