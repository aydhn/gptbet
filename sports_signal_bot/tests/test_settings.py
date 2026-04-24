from sports_signal_bot.config.settings import get_settings, Settings

def test_settings_load():
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.app.app_name == "SportsSignalBot"
