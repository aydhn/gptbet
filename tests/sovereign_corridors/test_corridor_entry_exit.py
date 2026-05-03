from sports_signal_bot.sovereign_corridors.corridors import build_corridor
from sports_signal_bot.sovereign_corridors.entries import evaluate_corridor_entry
from sports_signal_bot.sovereign_corridors.exits import evaluate_corridor_exit

def test_corridor_entry_exit():
    corridor = build_corridor("corr-1", "us-east", "eu-west", "review_visibility_corridor")
    entry = evaluate_corridor_entry(corridor, {"transfer_class": "review_context_transfer"})
    assert entry.status == "guard_pass"

    exit_rec = evaluate_corridor_exit(corridor, {})
    assert exit_rec.status == "guard_pass"

    corridor.corridor_status = "corridor_blocked"
    entry2 = evaluate_corridor_entry(corridor, {})
    assert entry2.status == "guard_block"
