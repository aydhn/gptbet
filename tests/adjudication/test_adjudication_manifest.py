import pytest
from sports_signal_bot.adjudication.manifests import ManifestBuilder
from sports_signal_bot.adjudication.contracts import AdjudicationSummaryRecord

def test_build_manifest():
    summary = AdjudicationSummaryRecord(
        open_cases=1, resolved_cases=0, unresolved_cases=0,
        cases_by_type={}, cases_by_severity={}, memory_entries_created=0,
        precedent_match_rate=0.0, feedback_accepted_count=0, feedback_rejected_count=0,
        urgent_backlog_count=0, secondary_review_required_count=0
    )

    man = ManifestBuilder.build_manifest(summary, ["c1"])
    assert man.manifest_id is not None
    assert "c1" in man.case_ids
