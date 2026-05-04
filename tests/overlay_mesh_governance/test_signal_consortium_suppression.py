import pytest
from sports_signal_bot.overlay_mesh_governance import (
    ConsortiumSignalRecord,
    ConsortiumProvenanceRecord,
    ConsortiumCorroborationRecord,
    ConsortiumSignalFreshnessBandRecord,
    validate_consortium_signal,
    suppress_consortium_signal
)

def test_validate_and_suppress_signal():
    sig = ConsortiumSignalRecord(
        signal_id="s1", source_member="m1", source_baseline_ref="b1",
        signal_family="f1",
        freshness_band=ConsortiumSignalFreshnessBandRecord(band_name="b1", description="desc"),
        provenance_confidence=ConsortiumProvenanceRecord(provenance_source="src", provenance_confidence=0.05),
        corroboration_band=ConsortiumCorroborationRecord(corroboration_band="band", corroborating_sources=[]),
        caveat_density=0.0,
        suppression_state="active",
        projection_targets=[]
    )
    res = validate_consortium_signal(sig)
    assert res.suppression_state == "suppressed"

    res2 = suppress_consortium_signal(sig, "manual")
    assert res2.suppression_state == "suppressed"
