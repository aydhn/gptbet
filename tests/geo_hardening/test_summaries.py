import pytest

from sports_signal_bot.geo_hardening.summaries import generate_geo_mesh_summary


def test_generate_geo_mesh_summary():
    result = generate_geo_mesh_summary()
    assert result is None
