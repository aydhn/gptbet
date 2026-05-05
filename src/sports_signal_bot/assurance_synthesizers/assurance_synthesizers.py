from typing import List, Optional, Dict
import uuid

from src.sports_signal_bot.assurance_synthesizers.contracts import (
    SovereignGovernanceAssuranceSynthesizerRecord,
    AssuranceSynthesisInputRecord,
    AssuranceSynthesisPassRecord,
    AssuranceBand,
    AssuranceSynthesisOutputRecord
)

def build_governance_assurance_synthesizer(
    synthesizer_family: str
) -> SovereignGovernanceAssuranceSynthesizerRecord:
    return SovereignGovernanceAssuranceSynthesizerRecord(
        assurance_synthesizer_id=f"synth_{uuid.uuid4().hex[:8]}",
        synthesizer_family=synthesizer_family,
        current_state="initializing"
    )

def register_assurance_synthesis_input(
    synthesizer: SovereignGovernanceAssuranceSynthesizerRecord,
    input_family: str,
    currentness_state: str,
    sovereignty_state: str,
    no_safe_visibility_state: str
) -> AssuranceSynthesisInputRecord:
    inp = AssuranceSynthesisInputRecord(
        assurance_input_id=f"inp_{uuid.uuid4().hex[:8]}",
        input_family=input_family,
        source_ref="ref",
        currentness_state=currentness_state,
        caveat_state="caveated",
        sovereignty_state=sovereignty_state,
        no_safe_visibility_state=no_safe_visibility_state
    )
    synthesizer.input_refs.append(inp.assurance_input_id)
    return inp

def compute_assurance_synthesis_band(
    synthesizer: SovereignGovernanceAssuranceSynthesizerRecord,
    inputs: List[AssuranceSynthesisInputRecord]
) -> AssuranceSynthesisOutputRecord:
    band = AssuranceBand.strong_bounded_assurance
    warnings = []

    for inp in inputs:
        if "stale" in inp.currentness_state:
            band = AssuranceBand.bounded_assurance_with_caveats
            warnings.append(f"Stale input {inp.assurance_input_id} caps assurance")

        if "no_safe" in inp.no_safe_visibility_state:
            # Further downgrade if no_safe applies
            if band == AssuranceBand.strong_bounded_assurance or band == AssuranceBand.bounded_assurance_with_caveats:
                band = AssuranceBand.review_only_assurance
            warnings.append("no_safe visibility forces review_only")

        if "deny" in inp.sovereignty_state:
            band = AssuranceBand.critically_fragile_assurance
            warnings.append("local deny sovereignty override failure")
            break

    out = AssuranceSynthesisOutputRecord(
        output_id=f"out_{uuid.uuid4().hex[:8]}",
        band=band,
        synthesizer_ref=synthesizer.assurance_synthesizer_id,
        warnings=warnings,
        preserved_caveat_refs=["caveat_1"]
    )
    synthesizer.output_refs.append(out.output_id)
    synthesizer.current_state = "synthesized"
    return out

def summarize_assurance_synthesizer(
    synthesizer: SovereignGovernanceAssuranceSynthesizerRecord,
    output: AssuranceSynthesisOutputRecord
) -> Dict[str, str]:
    return {
        "id": synthesizer.assurance_synthesizer_id,
        "family": synthesizer.synthesizer_family,
        "band": output.band.value,
        "warnings": str(len(output.warnings))
    }
