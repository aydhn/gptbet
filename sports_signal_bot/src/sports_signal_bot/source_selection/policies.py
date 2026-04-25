from typing import List, Dict, Any
from .contracts import SourceEligibilityRecord, SourceExclusionReasonRecord, SourcePolicyDefinition
from .metadata import SourceMetadataRecord

class BasePolicy:
    def __init__(self, definition: SourcePolicyDefinition):
        self.definition = definition
        self.name = definition.policy_name
        self.is_enabled = definition.is_enabled

    def evaluate(self,
                 metadata: SourceMetadataRecord,
                 eligibility: SourceEligibilityRecord,
                 context: Dict[str, Any]) -> None:
        pass # Base implementation does nothing

    def evaluate_group(self, records: List[SourceEligibilityRecord], context: Dict[str, Any]) -> None:
        pass # Base implementation does nothing


class BasicAvailabilityPolicy(BasePolicy):
    def evaluate(self, metadata: SourceMetadataRecord, eligibility: SourceEligibilityRecord, context: Dict[str, Any]) -> None:
        if not self.is_enabled: return

        if not metadata.is_prediction_available:
            eligibility.is_available = False
            eligibility.is_eligible = False
            eligibility.exclusion_reasons.append(
                SourceExclusionReasonRecord(reason_code="source_unavailable", details="Prediction not available for event.")
            )

        if metadata.has_invalid_probabilities:
            eligibility.is_eligible = False
            eligibility.exclusion_reasons.append(
                SourceExclusionReasonRecord(reason_code="invalid_probabilities", details="NaNs or out of bounds prob detected.")
            )

class QualityThresholdPolicy(BasePolicy):
    def evaluate(self, metadata: SourceMetadataRecord, eligibility: SourceEligibilityRecord, context: Dict[str, Any]) -> None:
        if not self.is_enabled or not eligibility.is_eligible: return

        min_trust = self.definition.parameters.get("min_trust_score", 0.3)
        min_cov = self.definition.parameters.get("min_recent_coverage", 0.5)
        max_model_age = self.definition.parameters.get("max_model_age_days", 30)

        if eligibility.trust_score and eligibility.trust_score.total_trust_score < min_trust:
            eligibility.is_eligible = False
            eligibility.exclusion_reasons.append(
                SourceExclusionReasonRecord(reason_code="low_trust_score", details=f"Trust score below {min_trust}")
            )

        if metadata.recent_coverage_rate < min_cov:
            eligibility.is_eligible = False
            eligibility.exclusion_reasons.append(
                SourceExclusionReasonRecord(reason_code="insufficient_recent_coverage", details=f"Coverage below {min_cov}")
            )

        if metadata.model_age_days > max_model_age:
            eligibility.is_eligible = False
            eligibility.exclusion_reasons.append(
                SourceExclusionReasonRecord(reason_code="stale_model", details=f"Model age > {max_model_age} days")
            )

class RegimeAwarePolicy(BasePolicy):
    def evaluate(self, metadata: SourceMetadataRecord, eligibility: SourceEligibilityRecord, context: Dict[str, Any]) -> None:
        if not self.is_enabled or not eligibility.is_eligible: return

        # Penalize if historically very poor in active regime
        if eligibility.trust_score and eligibility.trust_score.regime_fit_score < 0.2:
             # Only exclude if we have enough sample size (handled in trust score dampening mostly, but hard limit here)
             eligibility.is_eligible = False
             eligibility.exclusion_reasons.append(
                 SourceExclusionReasonRecord(reason_code="low_regime_evidence", details="Very poor regime fit.")
             )

class PreferredCalibratedPolicy(BasePolicy):
    def evaluate_group(self, records: List[SourceEligibilityRecord], context: Dict[str, Any]) -> None:
        if not self.is_enabled: return

        # If there are calibrated versions in a family, drop the uncalibrated ones if they exist
        families: Dict[str, List[SourceEligibilityRecord]] = {}
        for r in records:
            if r.is_eligible:
                families.setdefault(r.source_family, []).append(r)

        for family, fam_records in families.items():
            has_calibrated = any(context.get('metadata_map', {})[r.source_name].is_calibrated for r in fam_records)
            if has_calibrated:
                for r in fam_records:
                    if not context.get('metadata_map', {})[r.source_name].is_calibrated:
                        r.is_eligible = False
                        r.exclusion_reasons.append(
                            SourceExclusionReasonRecord(reason_code="replaced_by_calibrated_variant", details="Calibrated variant preferred.")
                        )

class FallbackSafetyPolicy(BasePolicy):
    def evaluate_group(self, records: List[SourceEligibilityRecord], context: Dict[str, Any]) -> None:
        if not self.is_enabled: return

        eligible_count = sum(1 for r in records if r.is_eligible)
        min_required = self.definition.parameters.get("minimum_eligible_sources", 1)

        if eligible_count < min_required:
            context['fallback_used'] = True
            # Attempt to rescue sources with fallback tags or best trust score
            fallback_sources = self.definition.parameters.get("fallback_source_priority", [])
            for r in records:
                if not r.is_eligible and (r.source_name in fallback_sources or r.source_family in fallback_sources):
                    # Rescue if not fundamentally broken
                    fatal_reasons = {"source_unavailable", "invalid_probabilities"}
                    if not any(ex.reason_code in fatal_reasons for ex in r.exclusion_reasons):
                        r.is_eligible = True
                        r.warnings.append("Rescued by FallbackSafetyPolicy.")
