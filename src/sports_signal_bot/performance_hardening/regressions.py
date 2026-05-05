from typing import Dict, Any, List
from .contracts import PerformanceRegressionRecord

def detect_performance_regressions(measurements: List[Dict[str, float]], baseline: Dict[str, float]) -> List[PerformanceRegressionRecord]:
    return []

def compare_to_baseline(current: Dict[str, float], baseline: Dict[str, float]) -> Dict[str, float]:
    return {"latency_diff": current.get("latency", 0) - baseline.get("latency", 0)}

def classify_regression_severity(diff: float) -> str:
    if diff > 50: return "critical"
    if diff > 10: return "high"
    return "low"

def summarize_performance_regressions(regressions: List[PerformanceRegressionRecord]) -> Dict[str, Any]:
    return {"total": len(regressions)}
