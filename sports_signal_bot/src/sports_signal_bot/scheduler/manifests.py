import json
import os
from .contracts import SchedulerManifest

class SchedulerManifestWriter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write(self, manifest: SchedulerManifest):
        path = os.path.join(self.output_dir, f"scheduler_manifest_{manifest.schedule_run_id}.json")
        with open(path, "w") as f:
            f.write(manifest.model_dump_json(indent=2))
