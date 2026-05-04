from sports_signal_bot.federation_ecosystem.hubs import evaluate_hub_admission

def test_hub_admission():
    adm = evaluate_hub_admission("pkt1", "reg1", "valid", "heavy")
    assert adm.admission_status == "admitted_caveated"

    adm2 = evaluate_hub_admission("pkt2", "reg1", "expired", "none")
    assert adm2.admission_status == "blocked_expired"
