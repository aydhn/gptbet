import pandas as pd
from typing import List
from sports_signal_bot.portfolio.contracts import PortfolioAllocationRecord, PortfolioCandidateRecord

def to_allocations_df(allocations: List[PortfolioAllocationRecord]) -> pd.DataFrame:
    if not allocations:
        return pd.DataFrame()

    data = []
    for a in allocations:
        # Handle dict or model_dump
        try:
            d = a.model_dump()
        except AttributeError:
            d = a.dict()
        data.append(d)

    return pd.DataFrame(data)

def to_candidates_df(candidates: List[PortfolioCandidateRecord]) -> pd.DataFrame:
    if not candidates:
        return pd.DataFrame()

    data = []
    for c in candidates:
        try:
            d = c.model_dump()
        except AttributeError:
            d = c.dict()
        data.append(d)

    return pd.DataFrame(data)
