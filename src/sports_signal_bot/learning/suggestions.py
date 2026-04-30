import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    PatternCandidateRecord,
    RuleSuggestionRecordV2,
    SuggestionFamily,
    SuggestionWarningRecord
)
from .extraction import RuleExtractor
from .scopes import ScopeManager
from .risks import RiskClassifier
from .confidence import ConfidenceScorer

class SuggestionGenerator:
    @staticmethod
    def generate_suggestion(candidate: PatternCandidateRecord) -> RuleSuggestionRecordV2:
        warnings = []

        # 1. Extract Structured Rule
        extraction = RuleExtractor.extract_structured_rule(candidate)

        # 2. Determine Scope
        scope = ScopeManager.build_suggestion_scope(extraction)
        scope = ScopeManager.narrow_scope_if_needed(scope)
        if "narrowed_from_unsafe" in scope.constraints:
            warnings.append(SuggestionWarningRecord(
                warning_code="SCOPE_NARROWED",
                message="Original scope was unsafe and has been narrowed.",
                severity="medium"
            ))

        # 3. Classify Risk
        action_type = extraction.action_block.get("type", "unknown")
        risk = RiskClassifier.classify_suggestion_risk(scope, candidate.component_family, action_type)

        # 4. Score Confidence
        confidence = ConfidenceScorer.compute_suggestion_confidence(candidate.support, risk.risk_level, scope.is_safe)

        # 5. Determine Mode
        mode = ConfidenceScorer.classify_recommendation_mode(confidence)
        if mode == "blocked":
             warnings.append(SuggestionWarningRecord(
                warning_code="SUGGESTION_BLOCKED",
                message="Suggestion is blocked due to unsafe confidence or scope.",
                severity="high"
            ))

        # Map generic component family to a specific SuggestionFamily
        # This is simplified; a real mapping would look at the condition and action details
        family_map = {
            "provider_trust": SuggestionFamily.provider_penalty_damper,
            "alias_resolution": SuggestionFamily.alias_resolution_memory,
            "threshold": SuggestionFamily.threshold_band_shift,
            "policy": SuggestionFamily.borderline_candidate_policy,
            "weighting": SuggestionFamily.stale_source_penalty_tuning
        }
        mapped_family = family_map.get(candidate.component_family, SuggestionFamily.stable_source_preference)

        return RuleSuggestionRecordV2(
            suggestion_id=str(uuid.uuid4()),
            suggestion_family=mapped_family,
            target_component_family=candidate.component_family,
            target_parameter_or_rule=action_type,
            proposed_change_type=action_type,
            current_value_snapshot=None, # Needs context
            proposed_value_or_rule=extraction.action_block.get("adjustment"),
            scope=scope,
            support_count=candidate.support.support_count,
            support_strength=candidate.support.strength,
            confidence_score=confidence,
            estimated_risk=risk,
            evidence_refs=[candidate.pattern_id],
            precedent_refs=[],
            structured_rule=extraction,
            recommendation_mode=mode,
            warnings=warnings
        )
