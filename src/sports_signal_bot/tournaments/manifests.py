from typing import List, Dict, Any
from .contracts import (
    TournamentManifest,
    TournamentRequestRecord,
    TournamentBatchRecord,
    ParetoFrontRecord,
    TournamentRankingRecord,
    CandidateScorecardRecord,
    CandidateShortlistRecord,
    ShortlistTier
)
import uuid

def build_tournament_manifest(
    request: TournamentRequestRecord,
    batch: TournamentBatchRecord,
    fronts: List[ParetoFrontRecord],
    rankings: List[TournamentRankingRecord],
    scorecards: List[CandidateScorecardRecord],
    recommendations: List[Any] # from recommendations.py
) -> TournamentManifest:

    shortlists = []

    # Group by tier
    tiers = {
        ShortlistTier.TIER_1_REVIEW_NOW: [],
        ShortlistTier.TIER_2_GOOD_BUT_NEEDS_MORE_EVIDENCE: [],
        ShortlistTier.TIER_3_EXPLORATORY: [],
        ShortlistTier.TIER_4_REJECT: []
    }

    rec_map = {r.candidate_id: r for r in recommendations}

    for rank in rankings:
        rec = rec_map.get(rank.candidate_id)
        if rec and rec.tier:
            tiers[rec.tier].append((rank, rec))

    for tier, items in tiers.items():
        if items:
            ranks = [item[0] for item in items]
            recs = [item[1] for item in items]
            shortlists.append(CandidateShortlistRecord(
                shortlist_id=str(uuid.uuid4()),
                tournament_id=request.tournament_id,
                tier=tier,
                ranked_candidates=ranks,
                recommendations=recs
            ))

    return TournamentManifest(
        manifest_id=str(uuid.uuid4()),
        tournament_id=request.tournament_id,
        request=request,
        batch=batch,
        pareto_fronts=fronts,
        rankings=rankings,
        scorecards=scorecards,
        shortlists=shortlists
    )
