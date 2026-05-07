import pytest
from src.sports_signal_bot.planetary_federation_hardening.audit_cadence import (
    build_global_audit_cadence_orchestration, simulate_audit_cadence,
    OrchestrationFamily, OrchestrationStatus, CadenceWindowRecord
)

def test_simulate_audit_cadence_verified():
    orch = build_global_audit_cadence_orchestration("orch-01", OrchestrationFamily.WORLDWIDE_FOLLOW_THE_SUN_CADENCE_ORCHESTRATION)
    orch.window_refs.append(CadenceWindowRecord("win-01", is_stale=False, has_ack=True))

    health = simulate_audit_cadence(orch)
    assert health.is_healthy
    assert health.status == OrchestrationStatus.ORCHESTRATION_VERIFIED

def test_simulate_audit_cadence_caveated():
    orch = build_global_audit_cadence_orchestration("orch-01", OrchestrationFamily.WORLDWIDE_FOLLOW_THE_SUN_CADENCE_ORCHESTRATION)
    orch.window_refs.append(CadenceWindowRecord("win-01", is_stale=True, has_ack=True))

    health = simulate_audit_cadence(orch)
    assert not health.is_healthy
    assert health.status == OrchestrationStatus.ORCHESTRATION_CAVEATED

def test_simulate_audit_cadence_blocked():
    orch = build_global_audit_cadence_orchestration("orch-01", OrchestrationFamily.WORLDWIDE_FOLLOW_THE_SUN_CADENCE_ORCHESTRATION)
    orch.window_refs.append(CadenceWindowRecord("win-01", is_stale=False, has_ack=False))

    health = simulate_audit_cadence(orch)
    assert not health.is_healthy
    assert health.status == OrchestrationStatus.ORCHESTRATION_BLOCKED
