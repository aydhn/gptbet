from typing import List, Dict
from .contracts import CandidateInputRecord

class FleetAwarenessEngine:
    @staticmethod
    def detect_supersessions(candidates: List[CandidateInputRecord]) -> Dict[str, str]:
        supersessions = {}
        grouped = {}
        for c in candidates:
            grouped.setdefault(c.target_family, []).append(c)

        for family, group in grouped.items():
            if len(group) < 2:
                continue

            group.sort(key=lambda x: (x.readiness_score, x.evidence_completeness), reverse=True)
            strongest = group[0]

            for weaker in group[1:]:
                if strongest.readiness_score > weaker.readiness_score + 0.2:
                    supersessions[weaker.candidate_release_id] = strongest.candidate_release_id

        return supersessions
