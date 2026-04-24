from sports_signal_bot.orchestration.runner import SmokeRunner

def test_smoke_runner():
    runner = SmokeRunner()
    result = runner.run()
    assert result["status"] == "success"
    assert "predictions" in result
