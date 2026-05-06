from typing import Dict, Any

def create_relocation_wave_checkpoint(wave_id: str, checkpoint_type: str) -> Dict[str, Any]:
    return {"wave_id": wave_id, "checkpoint_type": checkpoint_type, "status": "verified"}

def detect_relocation_wave_gaps(segments: list) -> list:
    gaps = []
    expected_id = 0
    for s in segments:
        if s.get("id", -1) != expected_id:
            gaps.append(expected_id)
        expected_id += 1
    return gaps

def diff_relocation_wave_outputs(source: dict, target: dict) -> dict:
    diff = {}
    for k, v in source.items():
        if target.get(k) != v:
            diff[k] = {"source": v, "target": target.get(k)}
    return diff

def summarize_relocation_wave_stage(stage: dict) -> Dict[str, Any]:
    return {"stage_id": stage.get("id"), "status": stage.get("status", "unknown")}
