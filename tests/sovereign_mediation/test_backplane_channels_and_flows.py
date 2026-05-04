from sports_signal_bot.sovereign_mediation.backplanes import build_signal_routing_backplane, add_backplane_channel

def test_backplane_creation():
    backplane = build_signal_routing_backplane("test_family")
    channel = add_backplane_channel(backplane, "seg_a", "seg_b")
    assert len(backplane.channel_refs) == 1
    assert channel.channel_status == "active"
