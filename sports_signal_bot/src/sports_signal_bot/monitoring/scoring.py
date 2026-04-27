from typing import Dict, List, Any
from sports_signal_bot.monitoring.contracts import (
    HealthCheckRecord,
    ComponentHealthRecord,
    HealthScoreRecord,
    HealthStatus,
    HealthSeverity
)

def map_severity_to_penalty(severity: HealthSeverity) -> float:
    mapping = {
        HealthSeverity.INFO: 0.0,
        HealthSeverity.WARNING: 5.0,
        HealthSeverity.ERROR: 20.0,
        HealthSeverity.CRITICAL: 50.0
    }
    return mapping.get(severity, 0.0)

def score_component_health(component_name: str, run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    if not checks:
        return ComponentHealthRecord(
            component_name=component_name, run_id=run_id, status=HealthStatus.UNKNOWN, score=0.0, checks=[]
        )

    total_checks = len(checks)
    failed = sum(1 for c in checks if c.status == HealthStatus.FAILED)
    degraded = sum(1 for c in checks if c.status == HealthStatus.DEGRADED)
    skipped = sum(1 for c in checks if c.status == HealthStatus.SKIPPED)

    score = 100.0
    for check in checks:
        if check.status in (HealthStatus.FAILED, HealthStatus.DEGRADED):
            penalty = map_severity_to_penalty(check.severity)
            score -= penalty

    score = max(0.0, min(100.0, score))

    status = HealthStatus.OK
    if failed > 0:
        if any(c.severity == HealthSeverity.CRITICAL for c in checks if c.status == HealthStatus.FAILED):
            status = HealthStatus.FAILED
        else:
            status = HealthStatus.DEGRADED
    elif degraded > 0:
        status = HealthStatus.DEGRADED

    if score == 0.0:
         status = HealthStatus.FAILED

    return ComponentHealthRecord(
        component_name=component_name, run_id=run_id, status=status, score=score,
        total_checks=total_checks, failed_checks=failed, degraded_checks=degraded,
        skipped_checks=skipped, checks=checks
    )

def score_data_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("data_health", run_id, checks)
def score_artifact_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("artifact_health", run_id, checks)
def score_inference_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("inference_health", run_id, checks)
def score_decision_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("decision_health", run_id, checks)
def score_dispatch_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("dispatch_health", run_id, checks)

def map_score_to_global_status(score: float, has_critical: bool) -> HealthStatus:
    if has_critical: return HealthStatus.FAILED
    if score >= 90.0: return HealthStatus.OK
    elif score >= 60.0: return HealthStatus.DEGRADED
    else: return HealthStatus.FAILED

def explain_global_health_score(score: float, penalties: List[str]) -> str:
    base = f"Global Health Score: {score:.1f}/100.0"
    if penalties: base += f". Penalties applied: {', '.join(penalties)}"
    return base

def combine_component_health_scores(run_id: str, components: Dict[str, ComponentHealthRecord], missing_critical_checks: bool = False) -> HealthScoreRecord:
    if not components: return HealthScoreRecord(run_id=run_id, global_status=HealthStatus.UNKNOWN)
    total_weight = len(components)
    weighted_sum = sum(comp.score for comp in components.values())
    global_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    penalties_applied = []

    if missing_critical_checks:
        global_score -= 30.0
        penalties_applied.append("missing_critical_checks (-30)")

    global_score = max(0.0, min(100.0, global_score))
    has_critical = any(c.status == HealthStatus.FAILED for comp in components.values() for c in comp.checks if c.severity == HealthSeverity.CRITICAL)

    global_status = map_score_to_global_status(global_score, has_critical)
    explanation = explain_global_health_score(global_score, penalties_applied)

    return HealthScoreRecord(run_id=run_id, global_score=global_score, global_status=global_status, components=components, missing_critical_checks=missing_critical_checks, penalties_applied=penalties_applied, explanation=explanation)
