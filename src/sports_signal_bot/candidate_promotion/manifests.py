from typing import List, Dict, Any
from .contracts import CandidateManifest, CandidateReleaseRecord

def save_candidate_manifest(manifest: CandidateManifest, path: str):
    """Saves candidate manifest to a json file."""
    with open(path, "w") as f:
        f.write(manifest.model_dump_json(indent=2))
