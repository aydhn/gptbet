from sports_signal_bot.inference.slots import SlotResolver


def test_slot_resolution():
    resolver = SlotResolver()

    # Test valid slot
    slot_def = resolver.resolve_slot_definition("evening")
    assert slot_def.slot_id == "evening"
    assert slot_def.event_inclusion_horizon_hours == 0
    assert slot_def.artifact_resolution_policy == "latest_stable"

    # Test fallback slot
    unknown_slot = resolver.resolve_slot_definition("non_existent")
    assert unknown_slot.slot_id == "non_existent"
    assert unknown_slot.lookahead_window_hours == 12  # Default
