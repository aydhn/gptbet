# Fallback to SequentialCap for now in tests
from sports_signal_bot.portfolio.strategies.sequential_cap import SequentialCapAllocation
class TieredActionClassAllocation(SequentialCapAllocation):
    pass
