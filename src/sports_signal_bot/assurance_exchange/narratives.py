import uuid
from typing import List, Dict
from .contracts import SovereignGovernanceNarrativeCompilerRecord, NarrativeInputRecord, NarrativeOutputRecord, WarningRecord

def build_governance_narrative_compiler(compiler_family: str) -> SovereignGovernanceNarrativeCompilerRecord:
    return SovereignGovernanceNarrativeCompilerRecord(
        narrative_compiler_id=f"gnc_{uuid.uuid4()}",
        compiler_family=compiler_family,
        input_refs=[],
        section_refs=[],
        verification_refs=[],
        audience_profile_refs=[],
        currentness_policy_ref="default_freshness",
        health_status="healthy",
        warnings=[]
    )

def register_narrative_input(compiler: SovereignGovernanceNarrativeCompilerRecord, input_family: str, state: str) -> NarrativeInputRecord:
    record = NarrativeInputRecord(
        narrative_input_id=f"ni_{uuid.uuid4()}",
        input_family=input_family,
        source_ref="source_ref",
        currentness_state=state,
        caveat_state="preserved",
        sovereignty_state="preserved",
        no_safe_visibility_state="explicit",
        warnings=[]
    )
    compiler.input_refs.append(record.narrative_input_id)
    return record

def compile_governance_narrative(compiler: SovereignGovernanceNarrativeCompilerRecord) -> NarrativeOutputRecord:
    status = "narrative_current_with_caps"
    if compiler.warnings:
        status = "narrative_caveated"

    return NarrativeOutputRecord(
        output_id=f"no_{uuid.uuid4()}",
        output_status=status
    )

def classify_narrative_output(output: NarrativeOutputRecord) -> str:
    return output.output_status

def summarize_narrative_output(output: NarrativeOutputRecord) -> Dict:
    return {
        "id": output.output_id,
        "status": output.output_status
    }
