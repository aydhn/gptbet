from typing import List, Dict
from sports_signal_bot.ratings.contracts import RatingUpdateRecord
def summarize_updates(updates: List[RatingUpdateRecord]) -> Dict[str, float]:
    total_movement = sum(abs(u.home_rating_diff) + abs(u.away_rating_diff) for u in updates)
    return {"total_updates": len(updates), "total_absolute_rating_movement": total_movement}
