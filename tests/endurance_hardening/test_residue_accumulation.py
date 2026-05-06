from sports_signal_bot.endurance_hardening.residues import sample_residue_accumulation

def test_sample_residue_accumulation():
    res = sample_residue_accumulation("test")
    assert res.sample_id == "sample_test"
