from typing import Dict, Any, List
from .contracts import LongHorizonRegressionRecord, LongHorizonBaselineRecord

def detect_long_horizon_regressions() -> List[LongHorizonRegressionRecord]:
    return []

def compare_long_horizon_baselines(baseline_a: LongHorizonBaselineRecord, baseline_b: LongHorizonBaselineRecord) -> Dict[str, Any]:
    return {"diff": {}}

def classify_long_horizon_regression(regression: LongHorizonRegressionRecord) -> str:
    return regression.severity

def summarize_long_horizon_regressions(regressions: List[LongHorizonRegressionRecord]) -> Dict[str, Any]:
    return {"regression_count": len(regressions)}
