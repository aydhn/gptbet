import uuid
from typing import List
from .contracts import LaneAutomationCandidateRecord, LoopClosureRecord, ClosureOutcome, RemediationLaneRecord

def identify_lane_automation_candidates(lanes: List[RemediationLaneRecord], closures: List[LoopClosureRecord]) -> List[LaneAutomationCandidateRecord]:
    candidates = []

    closure_map = {}
    for c in closures:
        if c.lane_ref not in closure_map:
            closure_map[c.lane_ref] = []
        closure_map[c.lane_ref].append(c)

    for lane in lanes:
        lane_closures = closure_map.get(lane.lane_id, [])
        clean_count = sum(1 for c in lane_closures if c.outcome == ClosureOutcome.closed_clean)
        caveat_count = sum(1 for c in lane_closures if c.outcome == ClosureOutcome.closed_with_caveats)

        if clean_count >= 1:
            caveat_ratio = caveat_count / (clean_count + caveat_count) if (clean_count + caveat_count) > 0 else 0

            candidates.append(LaneAutomationCandidateRecord(
                candidate_id=f"candidate_{uuid.uuid4().hex[:8]}",
                lane_family=lane.lane_family,
                scoped_playbook_ref=lane.scoped_playbook_ref,
                successful_closures=clean_count,
                caveat_ratio=caveat_ratio,
                is_approved_candidate=(caveat_ratio < 0.2),
                reasons=[f"Proven track record with {clean_count} clean closures."]
            ))

    return candidates
