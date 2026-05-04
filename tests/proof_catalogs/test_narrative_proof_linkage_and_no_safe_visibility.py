import pytest
from src.sports_signal_bot.proof_catalogs.integration import (
    build_narrative_proof_pipeline,
    connect_narratives_to_proof_catalog,
    summarize_narrative_proof_flow,
    enforce_phase93_currentness_caveat_scope_rules,
    explain_phase93_block_or_downgrade,
    preserve_local_deny_in_phase93_outputs,
    explain_sovereignty_phase93_effects
)

def test_pipeline():
    pipeline = build_narrative_proof_pipeline()
    assert pipeline == "narrative_proof_pipeline"
    summary = summarize_narrative_proof_flow()
    assert summary == "narrative_proof_flow_summary"

def test_enforce_rules():
    enforce_phase93_currentness_caveat_scope_rules()
    reason = explain_phase93_block_or_downgrade()
    assert reason == "downgraded_due_to_stale_proof"

def test_sovereignty_preservation():
    preserve_local_deny_in_phase93_outputs()
    effect = explain_sovereignty_phase93_effects()
    assert effect == "sovereignty_preserved"
