from .contracts import SynthesisPassRecord, GovernanceResilienceScoreSynthesisRecord

def execute_score_synthesis_passes(synthesis: GovernanceResilienceScoreSynthesisRecord, passes: list[SynthesisPassRecord]):
    for p in passes:
        synthesis.pass_refs.append(p.pass_id)

def compute_synthesis_dimensions() -> dict:
    return {"federated_health_quality": 1.0, "replay_support_quality": 1.0}
