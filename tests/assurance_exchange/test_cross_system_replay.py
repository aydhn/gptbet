from sports_signal_bot.assurance_exchange.replay import replay_external_assurance_packet
from sports_signal_bot.assurance_exchange.packets import build_exchange_packet

def test_replay_external_assurance_packet():
    packet = build_exchange_packet("pkt_1", "family", "src", ["b1"], ["c1"], [], [])
    replay = replay_external_assurance_packet("rep_1", packet, {"packet_id": "pkt_1"})
    assert replay.result == "replay_accepted"
