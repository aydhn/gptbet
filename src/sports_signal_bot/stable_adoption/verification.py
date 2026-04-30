from typing import List, Dict, Any
import datetime
from .contracts import PostActivationVerificationRecord, VerificationWindow, VerificationOutcomeType

def build_post_activation_verification_plan(adoption_id: str, window: VerificationWindow, checks: List[str]) -> PostActivationVerificationRecord:
    return PostActivationVerificationRecord(
        verification_id=f"verif_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        window=window,
        checks=checks,
        overall_outcome=VerificationOutcomeType.VERIFIED_CLEAN
    )

def run_post_activation_checks(plan: PostActivationVerificationRecord, simulated_results: Dict[str, bool]) -> PostActivationVerificationRecord:
    all_passed = True
    for check in plan.checks:
        if not simulated_results.get(check, False):
            all_passed = False
            break

    if all_passed:
        plan.overall_outcome = VerificationOutcomeType.VERIFIED_CLEAN
    else:
        plan.overall_outcome = VerificationOutcomeType.ROLLBACK_REQUIRED

    return plan

def detect_post_activation_regression(plan: PostActivationVerificationRecord) -> bool:
    return plan.overall_outcome in [VerificationOutcomeType.ROLLBACK_REQUIRED, VerificationOutcomeType.ROLLBACK_RECOMMENDED, VerificationOutcomeType.DEGRADED_BUT_TOLERABLE]

def summarize_verification_outcome(plan: PostActivationVerificationRecord) -> str:
    return f"Verification {plan.verification_id} outcome: {plan.overall_outcome.value} for {len(plan.checks)} checks."

def classify_verification_status(plan: PostActivationVerificationRecord) -> VerificationOutcomeType:
    return plan.overall_outcome
