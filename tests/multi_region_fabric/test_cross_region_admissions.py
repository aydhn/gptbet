from sports_signal_bot.multi_region_fabric.admissions import evaluate_cross_region_admission

def test_evaluate_cross_region_admission():
    adm = evaluate_cross_region_admission("l1", "us-east", "eu-west", True, True)
    assert adm.outcome == "external_transfer_preparation_allowed"

    adm2 = evaluate_cross_region_admission("l2", "us-east", "eu-west", False, True)
    assert adm2.outcome == "treaty_missing"
