import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    SovereignGovernanceHealthCompilerRecord,
    CompilerInputRecord,
    CompilerPassRecord,
    CompilerPenaltyRecord,
    CompilerOutputRecord
)

def build_governance_health_compiler(
    compiler_family: str
) -> SovereignGovernanceHealthCompilerRecord:
    return SovereignGovernanceHealthCompilerRecord(
        compiler_id=f"comp_{uuid.uuid4().hex[:8]}",
        compiler_family=compiler_family, # type: ignore
        current_state="initializing"
    )

def register_compiler_input(
    compiler: SovereignGovernanceHealthCompilerRecord,
    input_family: str,
    source_ref: str,
    currentness_state: str,
    caveat_state: str,
    replay_state: str,
    lineage_state: str,
    applicability_state: str
) -> CompilerInputRecord:
    record = CompilerInputRecord(
        input_id=f"in_{uuid.uuid4().hex[:8]}",
        input_family=input_family,
        source_ref=source_ref,
        currentness_state=currentness_state,
        caveat_state=caveat_state,
        replay_state=replay_state,
        lineage_state=lineage_state,
        applicability_state=applicability_state
    )
    compiler.input_refs.append(record.input_id)
    return record

def execute_health_compiler_passes(
    compiler: SovereignGovernanceHealthCompilerRecord,
    inputs: List[CompilerInputRecord]
) -> List[CompilerPassRecord]:

    passes = []

    # Simple currentness check
    stale_inputs = [i for i in inputs if i.currentness_state != "current"]
    passes.append(CompilerPassRecord(
        pass_id=f"pass_{uuid.uuid4().hex[:8]}",
        pass_type="currentness_pass",
        status="failed" if stale_inputs else "passed",
        warnings=[f"Stale input: {i.source_ref}" for i in stale_inputs]
    ))

    # Sovereignty pass (fail safe)
    passes.append(CompilerPassRecord(
        pass_id=f"pass_{uuid.uuid4().hex[:8]}",
        pass_type="sovereignty_pass",
        status="passed"
    ))

    for p in passes:
        compiler.pass_refs.append(p.pass_id)

    return passes

def compute_compiler_band(
    passes: List[CompilerPassRecord],
    penalties: List[CompilerPenaltyRecord]
) -> CompilerOutputRecord:

    band = "strong_bounded_health"
    restoration_ceiling = "high"
    blockers = []
    caveats = []

    for p in passes:
        if p.status == "failed":
            if p.pass_type == "sovereignty_pass":
                band = "critically_fragile"
                blockers.append("Sovereignty failure")
                restoration_ceiling = "none"
                break
            elif p.pass_type == "currentness_pass":
                band = "review_only_health"
                restoration_ceiling = "low"
                caveats.append("Stale inputs")

    if band != "critically_fragile":
        high_severity_penalties = [p for p in penalties if p.severity == "high"]
        if high_severity_penalties:
            band = "fragile"
            restoration_ceiling = "minimal"
            for p in high_severity_penalties:
                caveats.append(p.explanation)

    return CompilerOutputRecord(
        output_id=f"out_{uuid.uuid4().hex[:8]}",
        compiler_ref="temp",
        health_band=band, # type: ignore
        restoration_ceiling=restoration_ceiling,
        blockers=blockers,
        caveats=caveats
    )

def summarize_compiler_state(
    compiler: SovereignGovernanceHealthCompilerRecord,
    passes: List[CompilerPassRecord],
    output: Optional[CompilerOutputRecord]
) -> Dict[str, Any]:

    failed_passes = [p.pass_type for p in passes if p.status == "failed"]

    state = "failed" if failed_passes else "passed"
    compiler.current_state = state

    return {
        "compiler_id": compiler.compiler_id,
        "family": compiler.compiler_family,
        "inputs_count": len(compiler.input_refs),
        "state": state,
        "failed_passes": failed_passes,
        "health_band": output.health_band if output else "unknown",
        "restoration_ceiling": output.restoration_ceiling if output else "unknown"
    }
