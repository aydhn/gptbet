from sports_signal_bot.handoff.manifests import build_handoff_manifest
from sports_signal_bot.handoff.reporting import generate_handoff_summary

def test_build_handoff_manifest():
    summary = generate_handoff_summary([{"decision": "approve_handoff"}])
    manifest = build_handoff_manifest(packages=[], summary=summary)
    assert manifest.summary.total_candidates_evaluated == 1
    assert len(manifest.packages) == 0
