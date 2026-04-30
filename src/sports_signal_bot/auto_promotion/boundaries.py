from typing import List
from .contracts import CandidateInputRecord, ProgressionBlockerRecord

class SafetyBoundaryEvaluator:
    @staticmethod
    def evaluate_hard_blocks(candidate: CandidateInputRecord, config: dict) -> List[ProgressionBlockerRecord]:
        blockers = []

        # 1. Manual override / freeze
        if candidate.manual_override:
            blockers.append(ProgressionBlockerRecord(
                blocker_type="manual_override",
                reason=f"Active manual override overrides auto decision: {candidate.manual_override}",
                severity="critical"
            ))

        # 2. Stale Artifacts
        if candidate.simulation_freshness_hours > config.get("stale_simulation_block_hours", 24):
            blockers.append(ProgressionBlockerRecord(
                blocker_type="stale_simulation",
                reason=f"Simulation is {candidate.simulation_freshness_hours}h old (max {config.get('stale_simulation_block_hours', 24)}h)",
                severity="high"
            ))

        # 3. Disputed
        if candidate.dispute_count > 0:
            blockers.append(ProgressionBlockerRecord(
                blocker_type="unresolved_dispute",
                reason=f"{candidate.dispute_count} unresolved critical disputes block auto progression.",
                severity="high"
            ))

        # 4. Gates Fails
        if candidate.gate_cleanliness < 1.0:
            blockers.append(ProgressionBlockerRecord(
                blocker_type="failed_gates",
                reason="Quality gates not fully clean.",
                severity="high"
            ))

        return blockers

    @staticmethod
    def requires_approval(candidate: CandidateInputRecord) -> bool:
        return candidate.risk_level == "high" or candidate.scope_breadth == "broad"
