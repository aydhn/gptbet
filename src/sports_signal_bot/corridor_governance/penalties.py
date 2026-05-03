from sports_signal_bot.corridor_governance.contracts import SovereignInteroperabilityScorecardRecord

def apply_scorecard_penalties(scorecard: SovereignInteroperabilityScorecardRecord, penalties: float) -> SovereignInteroperabilityScorecardRecord:
    scorecard.overall_score -= penalties
    if scorecard.overall_score < 0:
        scorecard.overall_score = 0

    scorecard.overall_band = map_score_to_band(scorecard.overall_score)
    return scorecard

def map_score_to_band(score: float) -> str:
    from sports_signal_bot.corridor_governance.scorecards import map_score_to_band
    return map_score_to_band(score)
