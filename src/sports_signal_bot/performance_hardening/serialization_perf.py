from typing import Dict, Any

def measure_serialization_costs(obj: Any) -> Dict[str, float]:
    return {"duration_ms": 5.0, "bytes": 1024}

def compare_serialization_modes(obj: Any) -> Dict[str, Any]:
    return {"compact_ms": 2.0, "pretty_ms": 6.0}

def summarize_serialization_perf(measurements: list) -> Dict[str, Any]:
    return {"total_measurements": len(measurements)}
