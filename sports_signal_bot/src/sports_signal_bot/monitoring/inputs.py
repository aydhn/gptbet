import json
from pathlib import Path
from typing import Dict, Any, Optional

def _load_json_safe(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    try:
        with open(path, "r") as f: return json.load(f)
    except json.JSONDecodeError: return {}

def load_latest_inference_run(results_dir: str) -> Dict[str, Any]:
    base_dir = Path(results_dir)
    manifest_path = base_dir / "manifests" / "latest_inference_manifest.json"
    data = _load_json_safe(manifest_path)
    return {
        "event_universe_size": data.get("event_universe_size", 0),
        "approved_count": data.get("approved_count", 0),
        "no_action_count": data.get("no_action_count", 0),
        "total_actions": data.get("total_actions", 0),
        "fallback_count": data.get("fallback_count", 0),
        "feature_build_failures": data.get("feature_build_failures", 0),
        "model_age_days": data.get("model_age_days", 0),
        "stale_fixtures_count": data.get("stale_fixtures_count", 0),
        "missing_sources": data.get("missing_sources", []),
    }

def load_dispatch_health_inputs(results_dir: str) -> Dict[str, Any]:
    base_dir = Path(results_dir)
    dispatch_path = base_dir / "latest_dispatch_summary.json"
    data = _load_json_safe(dispatch_path)
    return {"dispatch_failure_rate": data.get("failure_rate", 0.0)}

def load_artifact_freshness_inputs(results_dir: str) -> Dict[str, Any]: return {}
def load_previous_health_runs(results_dir: str) -> list: return []

class MonitoringInputBuilder:
    def __init__(self, results_dir: str):
        self.results_dir = results_dir
    def build(self) -> Dict[str, Dict[str, Any]]:
        inference_inputs = load_latest_inference_run(self.results_dir)
        dispatch_inputs = load_dispatch_health_inputs(self.results_dir)
        return {"inference_health": inference_inputs, "decision_health": inference_inputs, "data_health": inference_inputs, "artifact_health": inference_inputs, "dispatch_health": dispatch_inputs, "portfolio_health": {}, "bankroll_health": {}}
