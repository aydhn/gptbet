from sports_signal_bot.assurance_exchange.strategies.conservative import ConservativeNarrativeAssuranceStrategy
from sports_signal_bot.assurance_exchange.strategies.balanced_board_clearing import BalancedBoardClearingStrategy

def test_conservative_strategy():
    strategy = ConservativeNarrativeAssuranceStrategy()
    assert strategy.apply_currentness_rules(2000) == "snapshot_stale"
    assert strategy.apply_board_clearing_rules() == "cleared_caveated_replay"

def test_balanced_strategy():
    strategy = BalancedBoardClearingStrategy()
    assert strategy.apply_currentness_rules(2000) == "snapshot_caveated"
    assert strategy.apply_currentness_rules(4000) == "snapshot_stale"
