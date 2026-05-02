from sports_signal_bot.assurance_exchange.integration import run_interop_verification
from sports_signal_bot.assurance_exchange.packets import build_exchange_packet

def test_run_interop_verification():
    packet = build_exchange_packet("pkt_1", "family", "src", ["b1"], ["c1"], [], [])
    res = run_interop_verification(packet, [])
    assert res["final_status"] == "verified"
