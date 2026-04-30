from typing import Optional
from .contracts import CandidateInputRecord, AutoKillDecisionRecord, AutoHoldDecisionRecord, KillReasonCode, HoldReasonCode
import uuid

class AutoDecisionEvaluator:
    @staticmethod
    def evaluate_kill(candidate: CandidateInputRecord, config: dict) -> Optional[AutoKillDecisionRecord]:
        confidence = 0.0
        reason = None
        failures = []

        if candidate.evidence_completeness < config.get("boundaries", {}).get("minimum_evidence_for_kill", 0.8):
            return None

        if candidate.gate_cleanliness < 0.5 and candidate.readiness_score < 0.4:
            reason = KillReasonCode.failed_required_quality_gates
            confidence = 0.85
            failures.append("Gate cleanliness and readiness critically low.")

        elif candidate.dispute_count > 3:
            reason = KillReasonCode.unresolved_critical_dispute
            confidence = 0.90
            failures.append("Excessive unresolved disputes.")

        if reason and confidence > 0.8:
            return AutoKillDecisionRecord(
                auto_kill_id=f"ak-{uuid.uuid4().hex[:8]}",
                candidate_release_id=candidate.candidate_release_id,
                kill_reason_code=reason,
                current_stage=candidate.current_stage,
                supporting_failures=failures,
                confidence_in_kill=confidence,
                reversible=True
            )
        return None

    @staticmethod
    def evaluate_hold(candidate: CandidateInputRecord, config: dict) -> Optional[AutoHoldDecisionRecord]:
        if 0.5 <= candidate.gate_cleanliness < 1.0:
            return AutoHoldDecisionRecord(
                auto_hold_id=f"ah-{uuid.uuid4().hex[:8]}",
                candidate_release_id=candidate.candidate_release_id,
                hold_reason_code=HoldReasonCode.missing_fresh_gate_results,
                current_stage=candidate.current_stage
            )

        if candidate.conflict_burden > 0:
            return AutoHoldDecisionRecord(
                auto_hold_id=f"ah-{uuid.uuid4().hex[:8]}",
                candidate_release_id=candidate.candidate_release_id,
                hold_reason_code=HoldReasonCode.unresolved_noncritical_conflicts,
                current_stage=candidate.current_stage
            )

        return None
