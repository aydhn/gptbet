from sports_signal_bot.multi_region_fabric.contentions import detect_cross_region_contentions

def test_detect_cross_region_contentions():
    cs = detect_cross_region_contentions(["us-east", "eu-west"])
    assert len(cs) == 1
    assert cs[0].outcome == "region_serialize"
