from typing import List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.core.constants import SportType


class MarketDefinition(BaseModel):
    market_type: str
    sport: SportType
    selection_schema: List[str]
    required_inputs: List[str]
    settlement_rule_name: str
    supports_push: bool = False
    supports_multiclass: bool = False
    supports_probabilities: bool = True
    notes: Optional[str] = None
