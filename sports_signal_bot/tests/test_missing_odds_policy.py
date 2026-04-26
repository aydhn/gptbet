from sports_signal_bot.bankroll.utils import handle_missing_odds
from sports_signal_bot.bankroll.contracts import MissingOddsPolicy
import pytest

def test_missing_odds():
    assert handle_missing_odds(MissingOddsPolicy.SKIP) == True
    assert handle_missing_odds(MissingOddsPolicy.PROXY) == False

    with pytest.raises(ValueError):
        handle_missing_odds(MissingOddsPolicy.FAIL)
