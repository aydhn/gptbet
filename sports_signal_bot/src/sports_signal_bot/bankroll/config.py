from pydantic import BaseModel

from sports_signal_bot.bankroll.contracts import BankrollConfig

# Placeholder for specific config overrides if needed in future
class FootballBankrollConfig(BankrollConfig):
    pass

class BasketballBankrollConfig(BankrollConfig):
    pass
