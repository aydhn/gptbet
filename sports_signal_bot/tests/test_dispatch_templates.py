import pytest
from sports_signal_bot.telegram_dispatch.templates import MessageTemplateEngine
from sports_signal_bot.telegram_dispatch.contracts import DispatchPayloadRecord

def test_render_decision_standard():
    engine = MessageTemplateEngine({"dispatch_profiles": {"standard": True}})
    payload = DispatchPayloadRecord(
        event_id="E1",
        market="1x2",
        sport="football",
        decision_class="approved",
        signal_score=0.85,
        edge=0.08,
        allocated_stake=2.5,
        rationale="Strong model agreement",
        warnings=["minor variance"]
    )

    res = engine.render_decision(payload, "run-1")
    assert "Decision: E1 \\| 1x2" in res
    assert "0\\.85" in res or "0.85" in res # Depending on escape logic applied
    assert "Strong model agreement" in res
    assert "minor variance" in res
