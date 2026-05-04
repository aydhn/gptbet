import pytest
from sports_signal_bot.overlay_mesh_governance import (
    ConsortiumSignalRecord,
    ConsortiumProvenanceRecord,
    ConsortiumCorroborationRecord,
    ConsortiumSignalFreshnessBandRecord,
    cap_signal_strength_by_provenance
)

def test_cap_signal_by_provenance():
    sig = ConsortiumSignalRecord(
        signal_id="s1", source_member="m1", source_baseline_ref="b1",
        signal_family="f1",
        freshness_band=ConsortiumSignalFreshnessBandRecord(band_name="b1", description="desc"),
        provenance_confidence=ConsortiumProvenanceRecord(provenance_source="src", provenance_confidence=0.1),
        corroboration_band=ConsortiumCorroborationRecord(corroboration_band="strong", corroborating_sources=[]),
        caveat_density=0.0,
        suppression_state="active",
        projection_targets=[]
    )
    res = cap_signal_strength_by_provenance(sig)
    # since provenance < 0.5, band should be capped
    assert res.corroboration_band.corroboration_band == "weakly_supported"
