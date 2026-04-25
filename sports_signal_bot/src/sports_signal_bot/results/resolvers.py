from typing import Callable, Dict, Optional

from sports_signal_bot.labels.contracts import LabelValidityStatus
from sports_signal_bot.results.contracts import EventResultRecord


def _check_missing_scores(result: EventResultRecord) -> Optional[LabelValidityStatus]:
    if result.final_home_score is None or result.final_away_score is None:
        if result.status.lower() in ["finished", "completed"]:
            return LabelValidityStatus.INVALID  # Finished but missing scores
        elif result.status.lower() in ["cancelled", "postponed"]:
            return LabelValidityStatus.VOID
        else:
            return LabelValidityStatus.PENDING
    return None


def resolve_1x2(
    result: EventResultRecord, line: Optional[float] = None
) -> (str, LabelValidityStatus, Optional[str]):
    status = _check_missing_scores(result)
    if status:
        return None, status, "Missing score or non-finished event"

    h = result.final_home_score
    a = result.final_away_score
    if h > a:
        return "home", LabelValidityStatus.VALID, None
    elif h < a:
        return "away", LabelValidityStatus.VALID, None
    else:
        return "draw", LabelValidityStatus.VALID, None


def resolve_over_under(
    result: EventResultRecord, line: Optional[float]
) -> (str, LabelValidityStatus, Optional[str]):
    if line is None:
        return None, LabelValidityStatus.UNSUPPORTED, "Line required for over_under"
    status = _check_missing_scores(result)
    if status:
        return None, status, "Missing score or non-finished event"

    total = result.final_home_score + result.final_away_score
    if total > line:
        return "over", LabelValidityStatus.VALID, None
    elif total < line:
        return "under", LabelValidityStatus.VALID, None
    else:
        return (
            "push",
            LabelValidityStatus.VOID,
            "Push not supported by default, voiding",
        )


def resolve_btts(
    result: EventResultRecord, line: Optional[float] = None
) -> (str, LabelValidityStatus, Optional[str]):
    status = _check_missing_scores(result)
    if status:
        return None, status, "Missing score or non-finished event"

    if result.final_home_score > 0 and result.final_away_score > 0:
        return "yes", LabelValidityStatus.VALID, None
    return "no", LabelValidityStatus.VALID, None


def resolve_basketball_moneyline(
    result: EventResultRecord, line: Optional[float] = None
) -> (str, LabelValidityStatus, Optional[str]):
    status = _check_missing_scores(result)
    if status:
        return None, status, "Missing score or non-finished event"

    h = result.final_home_score
    a = result.final_away_score
    if h > a:
        return "home", LabelValidityStatus.VALID, None
    elif h < a:
        return "away", LabelValidityStatus.VALID, None
    else:
        return (
            "push",
            LabelValidityStatus.VOID,
            "Draw not typical for moneyline, voiding",
        )


def resolve_basketball_totals(
    result: EventResultRecord, line: Optional[float]
) -> (str, LabelValidityStatus, Optional[str]):
    return resolve_over_under(result, line)


def resolve_basketball_spread(
    result: EventResultRecord, line: Optional[float]
) -> (str, LabelValidityStatus, Optional[str]):
    if line is None:
        return None, LabelValidityStatus.UNSUPPORTED, "Line required for spread"
    status = _check_missing_scores(result)
    if status:
        return None, status, "Missing score or non-finished event"

    h = result.final_home_score
    a = result.final_away_score

    # line is usually home spread. If line is -5.5, home needs to win by > 5.5
    # home_score + line > away_score
    adj_h = h + line
    if adj_h > a:
        return "home", LabelValidityStatus.VALID, None
    elif adj_h < a:
        return "away", LabelValidityStatus.VALID, None
    else:
        return "push", LabelValidityStatus.VOID, "Push"


# Registry for handlers
RESOLVER_REGISTRY: Dict[str, Callable] = {
    "football_1x2": resolve_1x2,
    "football_over_under": resolve_over_under,
    "football_btts": resolve_btts,
    "basketball_moneyline": resolve_basketball_moneyline,
    "basketball_totals": resolve_basketball_totals,
    "basketball_spread": resolve_basketball_spread,
}


def resolve_market(
    rule_name: str, result: EventResultRecord, line: Optional[float] = None
) -> (str, LabelValidityStatus, Optional[str]):
    handler = RESOLVER_REGISTRY.get(rule_name)
    if not handler:
        return (
            None,
            LabelValidityStatus.UNSUPPORTED,
            f"No settlement rule found for: {rule_name}",
        )
    return handler(result, line)
