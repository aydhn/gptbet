import json
from pathlib import Path
from typing import Dict, Any

from .contracts import (
    SovereignGovernanceTraceRouterManifestRecord,
    TraceRoutingSummary
)

def write_trace_routing_manifest(manifest: SovereignGovernanceTraceRouterManifestRecord, output_dir: str = "artifacts/") -> str:
    path = Path(output_dir) / "trace_routing_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(manifest.json(indent=2))
    return str(path)

def write_trace_routing_summary(summary: TraceRoutingSummary, output_dir: str = "artifacts/") -> str:
    path = Path(output_dir) / "trace_routing_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(summary.json(indent=2))
    return str(path)

def write_json_artifact(filename: str, data: Any, output_dir: str = "artifacts/") -> str:
    path = Path(output_dir) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        if hasattr(data, "json"):
            f.write(data.json(indent=2))
        else:
            json.dump(data, f, indent=2)
    return str(path)
