from .contracts import CandidateInputRecord, HeuristicScoreRecord

class EligibilityHeuristicsEngine:
    @staticmethod
    def compute_heuristic_score(candidate: CandidateInputRecord, config: dict) -> HeuristicScoreRecord:
        score = (candidate.readiness_score * 40.0) + (candidate.evidence_completeness * 30.0) + (candidate.gate_cleanliness * 30.0)

        components = {
            "base_readiness": candidate.readiness_score * 40.0,
            "base_evidence": candidate.evidence_completeness * 30.0,
            "base_gates": candidate.gate_cleanliness * 30.0
        }

        if candidate.risk_level == "low":
            bonus = config.get("heuristics", {}).get("low_risk_bonus", 10.0)
            score += bonus
            components["low_risk_bonus"] = bonus

        if candidate.conflict_burden > 0:
            penalty = config.get("heuristics", {}).get("conflict_penalty", -20.0) * candidate.conflict_burden
            score += penalty
            components["conflict_penalty"] = penalty

        if candidate.repeated_holds > 0:
            penalty = -5.0 * candidate.repeated_holds
            score += penalty
            components["repeated_hold_penalty"] = penalty

        return HeuristicScoreRecord(
            composite_score=max(0.0, min(100.0, score)),
            components=components
        )
