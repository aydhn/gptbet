import uuid
from typing import Dict, List
from datetime import datetime
from .contracts import (
    AdjudicationSummaryRecord,
    AdjudicationCaseRecord,
    AdjudicationCaseStatus,
    ResolutionRecord
)

class AdjudicationReporter:
    @staticmethod
    def summarize_adjudication_state(cases: List[AdjudicationCaseRecord], resolutions: List[ResolutionRecord]) -> AdjudicationSummaryRecord:
        open_cases = 0
        resolved_cases = 0
        unresolved_cases = 0
        cases_by_type = {}
        cases_by_severity = {}
        urgent_backlog = 0

        for c in cases:
            if c.current_status in [AdjudicationCaseStatus.queued, AdjudicationCaseStatus.in_review]:
                open_cases += 1
                if c.queue_priority.value == "urgent":
                    urgent_backlog += 1
            elif c.current_status in [AdjudicationCaseStatus.resolved, AdjudicationCaseStatus.resolved_with_caveat]:
                resolved_cases += 1
            elif c.current_status == AdjudicationCaseStatus.unresolved:
                unresolved_cases += 1

            t_val = c.case_type.value
            s_val = c.severity.value
            cases_by_type[t_val] = cases_by_type.get(t_val, 0) + 1
            cases_by_severity[s_val] = cases_by_severity.get(s_val, 0) + 1

        return AdjudicationSummaryRecord(
            open_cases=open_cases,
            resolved_cases=resolved_cases,
            unresolved_cases=unresolved_cases,
            cases_by_type=cases_by_type,
            cases_by_severity=cases_by_severity,
            memory_entries_created=0, # Placeholder
            precedent_match_rate=0.0,
            feedback_accepted_count=0,
            feedback_rejected_count=0,
            urgent_backlog_count=urgent_backlog,
            secondary_review_required_count=sum(1 for r in resolutions if "caveat" in r.caveats) # Rough proxy
        )
