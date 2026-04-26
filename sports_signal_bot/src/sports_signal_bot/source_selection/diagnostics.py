from collections import defaultdict
from typing import Dict, List

from .contracts import SourceEligibilitySummary, SourceSelectionDecision


class DiagnosticsBuilder:
    def build_summary(
        self, decisions: List[SourceSelectionDecision], context: Dict
    ) -> SourceEligibilitySummary:
        summary = SourceEligibilitySummary(
            total_candidates=len(decisions),
            fallback_used=context.get("fallback_used", False),
        )

        exclusion_counts: Dict[str, int] = defaultdict(int)
        family_totals: Dict[str, int] = defaultdict(int)
        family_eligible: Dict[str, int] = defaultdict(int)

        for d in decisions:
            family = d.eligibility_record.source_family
            family_totals[family] += 1

            if d.is_selected:
                summary.eligible_count += 1
                family_eligible[family] += 1
            else:
                summary.excluded_count += 1
                for ex in d.eligibility_record.exclusion_reasons:
                    exclusion_counts[ex.reason_code] += 1

            # Stale warnings
            if any("stale" in w.lower() for w in d.eligibility_record.warnings):
                summary.stale_source_warnings += 1

        summary.top_exclusion_reasons = dict(
            sorted(exclusion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        )

        for fam, total in family_totals.items():
            summary.family_eligibility_rates[fam] = family_eligible[fam] / total

        return summary
