from typing import List, Dict, Any, Tuple
from sports_signal_bot.capability_negotiation.contracts import (
    CapabilityProfileRecord,
    NegotiationDimensionResultRecord,
    CapabilityGapRecord,
    TranslationNeedRecord,
    NarrowingConstraintRecord,
    CapabilityDiffRecord,
    DimensionOutcome,
    DriftOutcome
)

def evaluate_negotiation_dimensions(
    source_profile: CapabilityProfileRecord,
    target_profile: CapabilityProfileRecord
) -> Tuple[List[NegotiationDimensionResultRecord], List[CapabilityGapRecord], List[TranslationNeedRecord], List[NarrowingConstraintRecord]]:
    dimensions = []
    gaps = []
    translation_needs = []
    narrowing_constraints = []

    # Simple matching logic for now
    def check_dimension(dim_name: str, source_list: List[str], target_list: List[str]):
        if not source_list and not target_list:
             return

        common = set(source_list).intersection(target_list)
        if set(source_list) == set(target_list) and source_list:
            dimensions.append(NegotiationDimensionResultRecord(dimension=dim_name, outcome=DimensionOutcome.exact_match, notes="Exact match"))
        elif common:
            dimensions.append(NegotiationDimensionResultRecord(dimension=dim_name, outcome=DimensionOutcome.narrower_support, notes="Partial match"))
            narrowing_constraints.append(NarrowingConstraintRecord(family=dim_name, narrowed_to=list(common)))
        else:
            dimensions.append(NegotiationDimensionResultRecord(dimension=dim_name, outcome=DimensionOutcome.unsupported, notes="No common capabilities"))
            gaps.append(CapabilityGapRecord(dimension=dim_name, gap_description=f"Source and target have no common {dim_name}"))

    check_dimension("artifact_families", source_profile.supported_artifact_families, target_profile.supported_artifact_families)
    check_dimension("claim_families", source_profile.supported_claim_families, target_profile.supported_claim_families)
    check_dimension("proof_formats", source_profile.supported_proof_formats, target_profile.supported_proof_formats)
    check_dimension("replay_modes", source_profile.supported_replay_modes, target_profile.supported_replay_modes)
    check_dimension("notarization_types", source_profile.supported_notarization_types, target_profile.supported_notarization_types)

    return dimensions, gaps, translation_needs, narrowing_constraints

def diff_capability_profiles(source: CapabilityProfileRecord, target: CapabilityProfileRecord) -> CapabilityDiffRecord:
    dims, gaps, translations, constraints = evaluate_negotiation_dimensions(source, target)
    return CapabilityDiffRecord(
        dimensions=dims,
        gaps=gaps,
        translation_needs=translations,
        narrowing_constraints=constraints
    )

def compute_capability_drift(old_profile: CapabilityProfileRecord, new_profile: CapabilityProfileRecord) -> CapabilityDiffRecord:
    return diff_capability_profiles(old_profile, new_profile)

def classify_capability_drift(diff: CapabilityDiffRecord) -> DriftOutcome:
    if not diff.gaps and not diff.narrowing_constraints:
        return DriftOutcome.compatible_drift

    if any(gap.dimension in ["proof_formats", "replay_modes"] for gap in diff.gaps):
        return DriftOutcome.federation_breaking_drift

    if diff.gaps:
        return DriftOutcome.blocking_drift

    return DriftOutcome.review_required_drift
