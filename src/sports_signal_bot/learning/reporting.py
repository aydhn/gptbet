from typing import List, Dict, Any
from .contracts import SuggestionManifest, SuggestionBundleRecord
from .contracts import LearningSummaryRecord

class LearningReporter:
    @staticmethod
    def generate_learning_summary(bundles: List[SuggestionBundleRecord], total_aggregates: int, total_candidates: int) -> LearningSummaryRecord:
        families = {}
        advisory_count = 0
        candidate_patch_count = 0
        high_risk_count = 0
        blocked_count = 0
        approval_req_count = 0

        for bundle in bundles:
            for sug in bundle.suggestions:
                fam = sug.suggestion_family.value
                families[fam] = families.get(fam, 0) + 1

                if sug.recommendation_mode == "advisory_only":
                    advisory_count += 1
                elif sug.recommendation_mode == "candidate_patch":
                    candidate_patch_count += 1
                elif sug.recommendation_mode == "blocked":
                    blocked_count += 1
                elif sug.recommendation_mode == "manual_review_required":
                    approval_req_count += 1

                if sug.estimated_risk.risk_level in ["high", "critical"]:
                    high_risk_count += 1

        total_suggestions = sum(families.values())

        return LearningSummaryRecord(
            total_feedback_aggregates=total_aggregates,
            pattern_candidate_count=total_candidates,
            generated_suggestions_count=total_suggestions,
            advisory_count=advisory_count,
            candidate_patch_count=candidate_patch_count,
            high_risk_suggestion_count=high_risk_count,
            low_support_suppressed_count=blocked_count,
            required_approval_count=approval_req_count,
            required_simulation_count=candidate_patch_count + approval_req_count,
            suggestions_by_family=families
        )

    @staticmethod
    def identify_unstable_families(summary: LearningSummaryRecord) -> List[str]:
        # Simple heuristic: if a family has many suggestions, it might be unstable
        unstable = []
        for fam, count in summary.suggestions_by_family.items():
            if count >= 5: # Arbitrary threshold for example
                unstable.append(fam)
        return unstable
