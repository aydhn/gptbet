import pytest
import json
from datetime import datetime, timezone
from sports_signal_bot.refresh_controller.contracts import RefreshManifest, RefreshProblem, FreezeStateRecord
from sports_signal_bot.refresh_controller.states import ProblemClass, ControllerState

def test_refresh_manifest_serialization():
    problem = RefreshProblem(
        problem_class=ProblemClass.DATA_FRESHNESS,
        severity="high",
        component="data",
        description="test"
    )

    freeze = FreezeStateRecord(
        freeze_reason="test",
        freeze_scope="global",
        auto_release_policy="manual"
    )

    manifest = RefreshManifest(
        detected_problems=[problem],
        chosen_plan=None,
        attempt=None,
        state_transitions=[],
        current_state=ControllerState.FROZEN,
        freeze_record=freeze,
        degrade_record=None
    )

    # Model serialization to json
    json_str = manifest.model_dump_json()
    assert "DATA_FRESHNESS" in json_str or "data_freshness" in json_str
    assert "frozen" in json_str
    assert "global" in json_str
