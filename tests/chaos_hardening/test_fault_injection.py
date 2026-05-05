import pytest
from sports_signal_bot.chaos_hardening.contracts import FaultInjectionPlanRecord

def test_fault_injection_plan():
    plan = FaultInjectionPlanRecord(plan_id="plan-1", events=[])
    assert plan.plan_id == "plan-1"
