from sports_signal_bot.geo_hardening.manifests import generate_geo_manifest


def test_manifest():
    assert generate_geo_manifest() is None
