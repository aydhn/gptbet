from typing import Any, Dict


def compute_rehearsal_symmetry(metrics: list) -> Dict[str, Any]:
    if not metrics:
        return {"symmetry_ratio": 1.0, "is_asymmetric": False}
    avg = sum(metrics) / len(metrics)
    is_asymmetric = any(abs(m - avg) > 0.1 for m in metrics)
    return {"symmetry_ratio": avg, "is_asymmetric": is_asymmetric}


def classify_divergence_severity(divergence: float) -> str:
    if divergence > 0.5:
        return "critical"
    elif divergence > 0.1:
        return "high"
    return "low"


def detect_dual_writer_risk(events: list) -> bool:
    writers = set()
    for e in events:
        if e.get("is_write"):
            writers.add(e.get("region"))
    return len(writers) > 1


def summarize_rehearsal_divergence(divergences: list) -> Dict[str, Any]:
    return {
        "total_divergences": len(divergences),
        "critical": sum(
            1 for d in divergences if classify_divergence_severity(d) == "critical"
        ),
    }
