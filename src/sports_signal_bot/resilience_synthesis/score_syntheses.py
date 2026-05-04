from typing import List

from .contracts import (
    GovernanceResilienceScoreSynthesisRecord,
    SynthesisInputRecord
)

def build_governance_resilience_score_synthesis(synthesis_id: str, family: str) -> GovernanceResilienceScoreSynthesisRecord:
    return GovernanceResilienceScoreSynthesisRecord(
        synthesis_id=synthesis_id,
        synthesis_family=family,
        current_state="initialized"
    )

def register_synthesis_input(
    synthesis: GovernanceResilienceScoreSynthesisRecord,
    input_id: str,
    source_ref: str,
    family: str = "default_input_family"
) -> SynthesisInputRecord:
    rec = SynthesisInputRecord(
        synthesis_input_id=input_id,
        input_family=family,
        source_ref=source_ref,
        currentness_state="fresh",
        caveat_state="none",
        replay_state="stable",
        convergence_state="converged",
        debt_state="clean"
    )
    synthesis.input_refs.append(input_id)
    return rec

def summarize_score_synthesis(synthesis: GovernanceResilienceScoreSynthesisRecord) -> dict:
    return {
        "id": synthesis.synthesis_id,
        "family": synthesis.synthesis_family,
        "inputs": len(synthesis.input_refs),
        "state": synthesis.current_state
    }
