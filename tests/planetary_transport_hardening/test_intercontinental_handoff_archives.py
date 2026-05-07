import pytest
from sports_signal_bot.planetary_transport_hardening import ConservativePlanetaryTransportHardeningStrategy, ArchiveStatus

def test_handoff_archive_pass():
    strat = ConservativePlanetaryTransportHardeningStrategy()
    res = strat.run_handoff_archive_pass({})
    assert len(res) == 1
    assert res[0].archive_status == ArchiveStatus.ARCHIVE_VERIFIED
    assert "follow_the_sun_handoff_archive" == res[0].archive_family
