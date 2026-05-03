from sports_signal_bot.multi_region_fabric.failover import evaluate_region_failover

def test_evaluate_region_failover():
    fo = evaluate_region_failover("us-east", "eu-west", True)
    assert fo.status == "failover_prepared"

    fo2 = evaluate_region_failover("us-east", "eu-west", False)
    assert fo2.status == "failover_blocked_revalidation"
