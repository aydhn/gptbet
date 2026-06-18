import datetime
from typing import Any, Dict, List, Optional

from .contracts import (AlignmentDimensionRecord, AlignmentInputRecord,
                        AlignmentOutputRecord, AlignmentPassRecord,
                        AlignmentPenaltyRecord,
                        GovernanceAlignmentCompilerWarningRecord,
                        SovereignGovernanceAlignmentCompilerRecord)


def build_governance_alignment_compiler(
    compiler_id: str, compiler_family: str
) -> SovereignGovernanceAlignmentCompilerRecord:
    """Builds a new sovereign governance alignment compiler."""
    return SovereignGovernanceAlignmentCompilerRecord(
        alignment_compiler_id=compiler_id,
        compiler_family=compiler_family,
        input_refs=[],
        pass_refs=[],
        dimension_refs=[],
        penalty_refs=[],
        ceiling_refs=[],
        output_refs=[],
        current_state="initialized",
        warnings=[],
    )


def register_alignment_input(
    compiler: SovereignGovernanceAlignmentCompilerRecord,
    input_record: AlignmentInputRecord,
) -> None:
    """Registers an input with the alignment compiler."""
    compiler.input_refs.append(input_record.alignment_input_id)
    if input_record.currentness_state == "stale":
        compiler.warnings.append(
            GovernanceAlignmentCompilerWarningRecord(
                "stale_input", f"Input {input_record.alignment_input_id} is stale."
            )
        )
    if input_record.no_safe_visibility_state == "hidden":
        compiler.warnings.append(
            GovernanceAlignmentCompilerWarningRecord(
                "no_safe_hidden",
                f"Input {input_record.alignment_input_id} hides no-safe visibility.",
            )
        )


def execute_alignment_compiler_passes(
    compiler: SovereignGovernanceAlignmentCompilerRecord,
    inputs: List[AlignmentInputRecord],
) -> List[AlignmentPassRecord]:
    """Executes the alignment passes."""
    passes = []

    # Example: Sovereignty Preservation Pass
    sovereignty_pass_result = "passed"
    for inp in inputs:
        if inp.sovereignty_state == "failed":
            sovereignty_pass_result = "failed"
            break
    passes.append(
        AlignmentPassRecord(
            pass_id="pass_sov_1",
            pass_type="sovereignty_preservation_pass",
            result=sovereignty_pass_result,
        )
    )

    # Example: No Safe Visibility Pass
    no_safe_pass_result = "passed"
    for inp in inputs:
        if inp.no_safe_visibility_state == "hidden":
            no_safe_pass_result = "failed"
            break
    passes.append(
        AlignmentPassRecord(
            pass_id="pass_no_safe_1",
            pass_type="no_safe_visibility_pass",
            result=no_safe_pass_result,
        )
    )

    compiler.pass_refs.extend(p.pass_id for p in passes)
    return passes


def summarize_alignment_compiler(
    compiler: SovereignGovernanceAlignmentCompilerRecord,
) -> Dict[str, str]:
    """Summarizes the alignment compiler state."""
    return {
        "compiler_id": compiler.alignment_compiler_id,
        "family": compiler.compiler_family,
        "inputs_count": str(len(compiler.input_refs)),
        "state": compiler.current_state,
    }


def compute_alignment_dimensions(
    inputs: List[AlignmentInputRecord],
) -> List[AlignmentDimensionRecord]:
    """Computes alignment dimensions based on inputs."""
    dimensions = []
    dimensions.append(
        AlignmentDimensionRecord(dimension_type="context_alignment", score=0.8)
    )
    dimensions.append(
        AlignmentDimensionRecord(dimension_type="sovereignty_preservation", score=1.0)
    )
    return dimensions


def apply_alignment_penalties(
    inputs: List[AlignmentInputRecord], passes: List[AlignmentPassRecord]
) -> List[AlignmentPenaltyRecord]:
    """Determines alignment penalties."""
    penalties = []
    for inp in inputs:
        if inp.currentness_state == "stale":
            penalties.append(
                AlignmentPenaltyRecord(
                    penalty_family="stale_context_penalty",
                    severity="high",
                    reason=f"Stale input {inp.alignment_input_id}",
                )
            )

    for p in passes:
        if p.pass_type == "no_safe_visibility_pass" and p.result == "failed":
            penalties.append(
                AlignmentPenaltyRecord(
                    penalty_family="no_safe_visibility_penalty",
                    severity="critical",
                    reason="No-safe visibility failed during pass.",
                )
            )

    return penalties


def compute_alignment_band(
    dimensions: List[AlignmentDimensionRecord],
    penalties: List[AlignmentPenaltyRecord],
    passes: List[AlignmentPassRecord],
) -> str:
    """Computes the final alignment band."""

    # Critical failures limit the band severely
    for p in passes:
        if p.pass_type == "sovereignty_preservation_pass" and p.result == "failed":
            return "critically_misaligned"

    for p in passes:
        if p.pass_type == "no_safe_visibility_pass" and p.result == "failed":
            return "review_only_alignment"

    # Evaluate penalties
    if any(p.severity == "critical" for p in penalties):
        return "review_only_alignment"

    if any(p.severity == "high" for p in penalties):
        return "bounded_alignment_with_caveats"

    return "strong_bounded_alignment"


def explain_alignment_output(output: AlignmentOutputRecord) -> str:
    """Explains the alignment output."""
    return f"Alignment Band: {output.alignment_band}. Preserved Caveats: {len(output.preserved_caveats)}. No-Safe Hints: {len(output.no_safe_recovery_hints)}."


def classify_alignment_penalties(
    penalties: List[AlignmentPenaltyRecord],
) -> Dict[str, int]:
    """Classifies alignment penalties by family."""
    classification = {}
    for p in penalties:
        classification[p.penalty_family] = classification.get(p.penalty_family, 0) + 1
    return classification


def attach_alignment_penalty_explanations(
    penalties: List[AlignmentPenaltyRecord],
) -> List[str]:
    """Generates explanations for the applied penalties."""
    return [f"{p.penalty_family} ({p.severity}): {p.reason}" for p in penalties]


def summarize_alignment_penalty_pressure(
    penalties: List[AlignmentPenaltyRecord],
) -> str:
    """Summarizes the total pressure from alignment penalties."""
    critical = sum(1 for p in penalties if p.severity == "critical")
    high = sum(1 for p in penalties if p.severity == "high")
    return f"Penalty Pressure: {critical} Critical, {high} High"
