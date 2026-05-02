import pytest
from sports_signal_bot.assurance.exceptions import block_illegal_exceptions

def test_exception_effects():
    assert block_illegal_exceptions([]) is True
