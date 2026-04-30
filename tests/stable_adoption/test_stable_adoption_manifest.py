import pytest
from sports_signal_bot.stable_adoption.manifests import build_adoption_manifest
from sports_signal_bot.stable_adoption.contracts import AdoptionSummaryRecord

def test_manifest_creation():
    summary = AdoptionSummaryRecord(summary_id="sum_01", candidate_count=1)
    manifest = build_adoption_manifest([], summary)
    assert manifest.summary.candidate_count == 1
