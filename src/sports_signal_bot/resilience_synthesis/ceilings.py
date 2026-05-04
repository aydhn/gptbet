from .contracts import SynthesisCeilingRecord, GovernanceResilienceScoreSynthesisRecord

def apply_synthesis_ceilings(synthesis: GovernanceResilienceScoreSynthesisRecord, ceilings: list[SynthesisCeilingRecord]):
    for c in ceilings:
        synthesis.ceiling_refs.append(c.ceiling_id)

def cap_phase89_outputs_due_to_replay_or_debt(band: str, debt_level: str, replay_status: str) -> str:
    if debt_level in ["critical", "high"] or replay_status == "blocked":
        if band in ["strong_bounded_resilience", "stabilized_resilience_with_caps"]:
            return "review_only_resilience"
    return band
