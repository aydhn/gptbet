from datetime import datetime, timedelta
from typing import List
from .contracts import (
    CohortVerificationWindowRecord, VerificationWindowType,
    VerificationSignalRecord, WindowOutcomeRecord, WindowOutcome,
    WindowRegressionSummaryRecord, WindowStabilityScoreRecord
)

def build_verification_windows(cohort_id: str, start_time: datetime) -> List[CohortVerificationWindowRecord]:
    return [
        CohortVerificationWindowRecord(
            cohort_id=cohort_id,
            window_type=VerificationWindowType.IMMEDIATE_WINDOW,
            started_at=start_time,
            ends_at=start_time + timedelta(hours=1)
        ),
        CohortVerificationWindowRecord(
            cohort_id=cohort_id,
            window_type=VerificationWindowType.SHORT_WINDOW,
            started_at=start_time,
            ends_at=start_time + timedelta(hours=24)
        )
    ]

def run_window_verification(window: CohortVerificationWindowRecord, signals: List[VerificationSignalRecord]) -> WindowOutcomeRecord:
    if not signals:
        return WindowOutcomeRecord(
            outcome_id=f"out_{window.cohort_id}_{window.window_type.value}",
            cohort_id=window.cohort_id,
            window_type=window.window_type,
            outcome=WindowOutcome.VERIFIED_WARNING
        )

    all_positive = all(s.is_positive for s in signals)
    outcome = WindowOutcome.VERIFIED_CLEAN if all_positive else WindowOutcome.REGRESSION_DETECTED

    return WindowOutcomeRecord(
        outcome_id=f"out_{window.cohort_id}_{window.window_type.value}",
        cohort_id=window.cohort_id,
        window_type=window.window_type,
        outcome=outcome
    )

def summarize_window_outcomes(outcomes: List[WindowOutcomeRecord]) -> dict:
    return {
        "total": len(outcomes),
        "clean": len([o for o in outcomes if o.outcome == WindowOutcome.VERIFIED_CLEAN]),
        "warnings": len([o for o in outcomes if o.outcome == WindowOutcome.VERIFIED_WARNING]),
        "regressions": len([o for o in outcomes if o.outcome == WindowOutcome.REGRESSION_DETECTED]),
        "rollbacks_required": len([o for o in outcomes if o.outcome == WindowOutcome.ROLLBACK_REQUIRED])
    }

def compute_window_stability(cohort_id: str, outcomes: List[WindowOutcomeRecord]) -> WindowStabilityScoreRecord:
    if not outcomes:
        score = 0.0
    else:
        clean_count = len([o for o in outcomes if o.outcome == WindowOutcome.VERIFIED_CLEAN])
        score = clean_count / len(outcomes)

    return WindowStabilityScoreRecord(
        score_id=f"stab_{cohort_id}",
        cohort_id=cohort_id,
        window_type=VerificationWindowType.STABILITY_WINDOW,
        score=score
    )

def run_autonomous_post_activation_verification(cohort_id: str) -> None:
    pass

def detect_verification_regressions(cohort_id: str) -> List[str]:
    return []

def emit_verification_alerts(cohort_id: str) -> None:
    pass
