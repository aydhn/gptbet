from sports_signal_bot.sovereign_corridors.treaties import build_treaty_backed_corridor, validate_corridor_against_treaty
from sports_signal_bot.sovereign_corridors.corridors import build_corridor

def test_treaty_corridors():
    corridor = build_corridor("corr-1", "src", "tgt", "family_1", treaty_ref="treaty-1")
    rec = build_treaty_backed_corridor("treaty-1", "corr-1", {"limit": 1})
    assert rec.corridor_ref == "corr-1"

    assert validate_corridor_against_treaty(corridor, {"treaty_id": "treaty-1"})
    assert not validate_corridor_against_treaty(corridor, {"treaty_id": "treaty-2"})
