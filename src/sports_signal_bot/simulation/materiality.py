from .contracts import MaterialityBand
from typing import List
from .contracts import BeforeAfterMetricRecord

def compute_materiality_score(metrics: List[BeforeAfterMetricRecord]) -> float:
    # simple sum of absolute deltas as a mock score
    return sum(abs(m.delta) for m in metrics)

def classify_materiality_band(score: float) -> MaterialityBand:
    if score < 1.0:
        return MaterialityBand.TRIVIAL
    elif score < 5.0:
        return MaterialityBand.SMALL
    elif score < 15.0:
        return MaterialityBand.MODERATE
    elif score < 30.0:
        return MaterialityBand.LARGE
    else:
        return MaterialityBand.CRITICAL
