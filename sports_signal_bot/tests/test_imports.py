def test_imports():
    import sports_signal_bot
    from sports_signal_bot.main import app
    from sports_signal_bot.config.settings import get_settings
    from sports_signal_bot.orchestration.runner import SmokeRunner
    assert True
