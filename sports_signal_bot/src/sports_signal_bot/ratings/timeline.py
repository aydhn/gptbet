from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
from sports_signal_bot.ratings.base import BaseRatingEngine
from sports_signal_bot.ratings.contracts import (RatingConfig,
                                                 RatingSnapshotRecord,
                                                 RatingUpdateRecord,
                                                 TeamRatingState)
from sports_signal_bot.results.contracts import EventResultRecord

logger = get_logger(__name__)


class RatingTimelineProcessor:
    def __init__(self, engine: BaseRatingEngine, config: RatingConfig):
        self.engine = engine
        self.config = config
        self._state_store: Dict[str, TeamRatingState] = {}
        self.snapshots: List[RatingSnapshotRecord] = []
        self.updates: List[RatingUpdateRecord] = []

    def _get_state_key(self, team_id: str, sport: str, league: str, season: str) -> str:
        mode = self.config.scope_mode
        if mode == "global":
            return f"{team_id}:{sport}"
        elif mode == "sport_league":
            return f"{team_id}:{sport}:{league}"
        elif mode == "sport_league_season":
            return f"{team_id}:{sport}:{league}:{season}"
        return f"{team_id}:{sport}:{league}"

    def _get_or_create_state(
        self, team_id: str, sport: str, league: str, season: str
    ) -> TeamRatingState:
        key = self._get_state_key(team_id, sport, league, season)
        if key not in self._state_store:
            self._state_store[key] = TeamRatingState(
                team_id=team_id,
                sport=sport,
                league=league,
                season=season,
                current_rating=self.config.base_rating,
            )
        return self._state_store[key]

    def _sort_events(self, df_events: pd.DataFrame) -> pd.DataFrame:
        return df_events.sort_values(
            by=["event_datetime_utc", "event_id"], ascending=[True, True]
        )

    def process_timeline(
        self, events: List[CanonicalEventRecord], results: List[EventResultRecord]
    ) -> Tuple[List[RatingSnapshotRecord], List[RatingUpdateRecord]]:
        if not events:
            return [], []
        df_e = pd.DataFrame([e.model_dump() for e in events])
        df_r = pd.DataFrame([r.model_dump() for r in results])
        if df_r.empty:
            df_merged = df_e
            df_merged["final_home_score"] = None
            df_merged["final_away_score"] = None
        else:
            df_merged = pd.merge(
                df_e,
                df_r[["event_id", "final_home_score", "final_away_score"]],
                on="event_id",
                how="left",
            )
        df_sorted = self._sort_events(df_merged)

        for _, row in df_sorted.iterrows():
            sport_val = (
                row["sport"].value
                if hasattr(row["sport"], "value")
                else str(row["sport"])
            )
            home_state = self._get_or_create_state(
                row["home_team"], sport_val, row["league"], row["season"]
            )
            away_state = self._get_or_create_state(
                row["away_team"], sport_val, row["league"], row["season"]
            )
            is_neutral = row.get("venue") == "neutral"
            exp_h, exp_a = self.engine.calculate_expected_outcome(
                home_state.current_rating, away_state.current_rating, is_neutral
            )

            snapshot = RatingSnapshotRecord(
                event_id=row["event_id"],
                sport=row["sport"],
                league=row["league"],
                season=row["season"],
                event_datetime_utc=row["event_datetime_utc"],
                home_team_id=row["home_team"],
                away_team_id=row["away_team"],
                is_neutral=is_neutral,
                pre_home_rating=home_state.current_rating,
                pre_away_rating=away_state.current_rating,
                home_advantage_applied=(
                    self.config.home_advantage if not is_neutral else 0.0
                ),
                expected_home_score=exp_h,
                expected_away_score=exp_a,
            )
            self.snapshots.append(snapshot)

            h_score = row.get("final_home_score")
            a_score = row.get("final_away_score")
            status = row.get("status", "").lower()
            if (
                pd.notna(h_score)
                and pd.notna(a_score)
                and status in ["completed", "finished", "closed"]
            ):
                h_pre, a_pre = home_state.current_rating, away_state.current_rating
                h_state, a_state, h_diff, a_diff = self.engine.apply_updates(
                    home_state, away_state, float(h_score), float(a_score), is_neutral
                )
                home_state.last_updated_utc = row["event_datetime_utc"]
                away_state.last_updated_utc = row["event_datetime_utc"]
                update = RatingUpdateRecord(
                    event_id=row["event_id"],
                    sport=row["sport"],
                    event_datetime_utc=row["event_datetime_utc"],
                    home_team_id=row["home_team"],
                    away_team_id=row["away_team"],
                    actual_home_score=float(h_score),
                    actual_away_score=float(a_score),
                    pre_home_rating=h_pre,
                    pre_away_rating=a_pre,
                    post_home_rating=home_state.current_rating,
                    post_away_rating=away_state.current_rating,
                    home_rating_diff=h_diff,
                    away_rating_diff=a_diff,
                )
                self.updates.append(update)
        return self.snapshots, self.updates

    def apply_season_transition(
        self, prev_season_states: List[TeamRatingState], new_season: str
    ) -> None:
        carryover = self.config.season_carryover
        base = self.config.base_rating
        for state in prev_season_states:
            new_rating = base + (state.current_rating - base) * carryover
            new_state = TeamRatingState(
                team_id=state.team_id,
                sport=state.sport,
                league=state.league,
                season=new_season,
                current_rating=new_rating,
                matches_played=0,
                last_updated_utc=None,
            )
            sport_val = (
                state.sport.value if hasattr(state.sport, "value") else str(state.sport)
            )
            key = self._get_state_key(
                state.team_id, sport_val, state.league, new_season
            )
            self._state_store[key] = new_state

    def get_latest_state(
        self, team_id: str, sport: str, league: str, season: str
    ) -> Optional[TeamRatingState]:
        key = self._get_state_key(team_id, sport, league, season)
        return self._state_store.get(key)
