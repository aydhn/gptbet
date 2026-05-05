import pytest
from sports_signal_bot.chaos_hardening.contracts import ChaosProbeRunRecord, ChaosWarningRecord

def test_chaos_probe_creation():
    probe = ChaosProbeRunRecord(
        chaos_probe_run_id="probe-1",
        run_family="timeout_storm_scenario",
        scenario_refs=["sc-1"],
        injected_fault_refs=["fault-1"],
        seed_ref="seed-1",
        environment_hash="env-1",
        observed_effect_refs=["eff-1"],
        outcome_status="degraded_honestly",
        residue_refs=[],
        warnings=[ChaosWarningRecord(warning_id="w1", severity="low", message="test")]
    )
    assert probe.chaos_probe_run_id == "probe-1"
    assert probe.outcome_status == "degraded_honestly"
