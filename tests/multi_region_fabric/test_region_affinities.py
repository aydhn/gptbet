from sports_signal_bot.multi_region_fabric.affinities import resolve_region_affinity, enforce_affinity_at_admission

def test_resolve_region_affinity():
    aff = resolve_region_affinity("a1", "hard_local_affinity")
    assert aff.affinity_type == "hard_local_affinity"
    assert not enforce_affinity_at_admission(aff, "eu-west")
