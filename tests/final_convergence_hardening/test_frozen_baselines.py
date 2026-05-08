from src.sports_signal_bot.final_convergence_hardening import (
    build_frozen_baseline,
    BaselineInputRecord,
    BaselineScopeRecord,
    verify_frozen_baseline,
    BaselineFreshnessRecord
)

def test_frozen_baseline_build_and_verify():
    inputs = [BaselineInputRecord(input_id="1", description="test")]
    scopes = [BaselineScopeRecord(scope_id="1", scope_type="test")]
    baseline = build_frozen_baseline("release_gating_baseline", inputs, scopes)
    assert baseline.baseline_status == "baseline_verified"
    assert verify_frozen_baseline(baseline)

def test_stale_baseline_fails_verification():
    inputs = [BaselineInputRecord(input_id="1", description="test")]
    scopes = [BaselineScopeRecord(scope_id="1", scope_type="test")]
    baseline = build_frozen_baseline("release_gating_baseline", inputs, scopes)
    baseline.freshness_refs.append(BaselineFreshnessRecord(freshness_id="1", is_stale=True))
    assert not verify_frozen_baseline(baseline)
