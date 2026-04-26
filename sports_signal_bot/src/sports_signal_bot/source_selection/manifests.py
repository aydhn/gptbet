from pathlib import Path

from .contracts import SourceSelectionManifest


class ManifestWriter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_manifest(self, manifest: SourceSelectionManifest) -> Path:
        run_dir = self.base_dir / manifest.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = run_dir / f"selection_manifest_{manifest.event_id}.json"

        with open(manifest_path, "w") as f:
            f.write(manifest.model_dump_json(indent=2))

        return manifest_path
