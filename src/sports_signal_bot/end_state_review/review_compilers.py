from typing import List, Optional
from .contracts import (
    SovereignGovernanceEndStateReviewCompilerRecord,
    EndStateReviewInputRecord,
    EndStateReviewPassRecord,
    EndStateReviewPenaltyRecord,
    EndStateReviewDimensionRecord,
    EndStateReviewBand
)

def build_governance_end_state_review_compiler(compiler_id: str, family: str) -> SovereignGovernanceEndStateReviewCompilerRecord:
    return SovereignGovernanceEndStateReviewCompilerRecord(
        end_state_review_compiler_id=compiler_id,
        compiler_family=family,
        input_refs=[],
        pass_refs=[],
        dimension_refs=[],
        penalty_refs=[],
        ceiling_refs=[],
        output_refs=[],
        closure_refs=[],
        current_state="initialized",
        warnings=[]
    )

def register_end_state_review_input(compiler: SovereignGovernanceEndStateReviewCompilerRecord, input_record: EndStateReviewInputRecord) -> None:
    compiler.input_refs.append(input_record.review_input_id)
    if input_record.currentness_state == "stale":
        compiler.warnings.append("stale_input_registered")

def execute_end_state_review_passes(compiler: SovereignGovernanceEndStateReviewCompilerRecord) -> None:
    compiler.current_state = "passes_executed"

def summarize_end_state_review_compiler(compiler: SovereignGovernanceEndStateReviewCompilerRecord) -> str:
    return f"Compiler {compiler.end_state_review_compiler_id} state: {compiler.current_state}"

def compute_end_state_review_dimensions(inputs: List[EndStateReviewInputRecord]) -> List[EndStateReviewDimensionRecord]:
    return []

def apply_end_state_review_penalties(compiler: SovereignGovernanceEndStateReviewCompilerRecord, penalties: List[EndStateReviewPenaltyRecord]) -> None:
    for p in penalties:
        compiler.penalty_refs.append(p.penalty_id)
        compiler.warnings.append(f"Penalty applied: {p.family}")

def compute_end_state_review_band(compiler: SovereignGovernanceEndStateReviewCompilerRecord) -> EndStateReviewBand:
    if "stale_input_registered" in compiler.warnings:
        return EndStateReviewBand.bounded_end_state_with_caveats
    return EndStateReviewBand.mature_bounded_end_state

def explain_end_state_review_output(band: EndStateReviewBand) -> str:
    return f"End state band is {band.value}"

def classify_end_state_review_penalties(penalties: List[EndStateReviewPenaltyRecord]) -> None:
    pass

def attach_review_penalty_explanations(penalties: List[EndStateReviewPenaltyRecord]) -> None:
    pass

def summarize_review_penalty_pressure(penalties: List[EndStateReviewPenaltyRecord]) -> str:
    return f"Total penalties applied: {len(penalties)}"
