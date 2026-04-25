import pytest

from sports_signal_bot.regimes.inputs import (build_event_regime_inputs,
                                              validate_regime_input_coverage)


def test_input_builder_and_validation():
    inputs = build_event_regime_inputs(
        event_id="1", sport="football", market_type="1x2", features={"a": 1}
    )
    assert inputs.event_id == "1"

    warnings = validate_regime_input_coverage(inputs, ["a", "b"])
    assert len(warnings) == 1
    assert "Missing required feature: b" in warnings[0]
