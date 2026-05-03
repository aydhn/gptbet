from sports_signal_bot.multi_region_fabric.sovereignty import resolve_sovereignty_policy, validate_sovereignty_boundary

def test_resolve_sovereignty_policy():
    policy = resolve_sovereignty_policy("p1", "us-domain")
    assert validate_sovereignty_boundary(policy, "export")
