from .contracts import SynthesisPenaltyRecord, GovernanceResilienceScoreSynthesisRecord

def apply_synthesis_penalties(synthesis: GovernanceResilienceScoreSynthesisRecord, penalties: list[SynthesisPenaltyRecord]):
    for p in penalties:
        synthesis.penalty_refs.append(p.penalty_id)

def classify_synthesis_penalties(penalties: list[SynthesisPenaltyRecord]) -> dict:
    return {p.penalty_family: p.impact for p in penalties}

def attach_synthesis_penalty_explanations(penalty: SynthesisPenaltyRecord) -> str:
    return f"Penalty {penalty.penalty_family} applied. Impact: {penalty.impact}"

def summarize_synthesis_penalty_pressure(penalties: list[SynthesisPenaltyRecord]) -> float:
    return sum(0.1 for p in penalties if p.impact == "high") # Dummy calculation
