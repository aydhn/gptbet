import pytest
from sports_signal_bot.simulation.patches import build_candidate_patch
from sports_signal_bot.simulation.contracts import PatchType, RiskLevel

def test_build_candidate_patch():
    suggestion = {
        "suggestion_id": "sug_123",
        "target_component_family": "provider_priority",
        "patch_type": "config_value_override",
        "patch_payload": {"new_weight": 0.8},
        "scope": {"provider": "bookmaker_a"}
    }
    patch = build_candidate_patch(suggestion)
    assert patch.suggestion_id == "sug_123"
    assert patch.patch_type == PatchType.CONFIG_VALUE_OVERRIDE
    assert patch.risk_level == RiskLevel.HIGH
    assert patch.sandbox_only is True
