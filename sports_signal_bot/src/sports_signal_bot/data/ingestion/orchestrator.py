import logging
import uuid
from datetime import datetime, timezone

from sports_signal_bot.core.constants import SportType
from sports_signal_bot.data.contracts.canonical import (
    CanonicalEventRecord, CanonicalOddsRecord, CanonicalTeamStatsRecord)
from sports_signal_bot.data.contracts.manifests import (IngestManifestRecord,
                                                        ValidationIssueRecord)
from sports_signal_bot.data.normalization.datetimes import \
    parse_datetime_to_utc
from sports_signal_bot.data.normalization.markets import normalize_market_name
from sports_signal_bot.data.normalization.names import normalize_league_name
from sports_signal_bot.data.providers.base import (BaseFixtureProvider,
                                                   BaseOddsProvider,
                                                   BaseStatsProvider)
from sports_signal_bot.data.storage.paths import (get_manifest_storage_path,
                                                  get_processed_storage_path,
                                                  get_raw_storage_path)
from sports_signal_bot.data.storage.writer import DataWriter
from sports_signal_bot.data.validators.odds_validator import \
    OddsSanityValidator
from sports_signal_bot.data.validators.schema_validator import (
    RequiredFieldsValidator, UniqueEventValidator)

logger = logging.getLogger(__name__)


class IngestionOrchestrator:
    def __init__(self, team_resolver=None):
        self.team_resolver = team_resolver

    def _generate_ingest_id(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S_") + str(uuid.uuid4())[:8]

    def _resolve_team(self, name: str, sport: str, league: str) -> str:
        if self.team_resolver:
            return self.team_resolver.resolve_team_name(name, sport, league)
        return name

    def ingest_fixtures(
        self, provider: BaseFixtureProvider, sport: SportType
    ) -> IngestManifestRecord:
        ingest_id = self._generate_ingest_id()
        logger.info(
            f"Starting fixture ingestion {ingest_id} for {sport.value} via {provider.provider_name}"
        )

        # 1. Fetch Raw
        raw_data = provider.fetch_fixtures(sport)
        raw_path = get_raw_storage_path(provider.provider_name, sport, "fixtures")
        DataWriter.write_json(raw_data, raw_path, f"{ingest_id}_raw.json")

        # 2. Normalize to Canonical format internally (dicts)
        normalized_data = []
        normalization_issues = []
        for idx, row in enumerate(raw_data):
            try:
                league = normalize_league_name(row.get("league", "unknown"))
                home_team = self._resolve_team(
                    row.get("home_team", ""), sport.value, league
                )
                away_team = self._resolve_team(
                    row.get("away_team", ""), sport.value, league
                )
                dt = parse_datetime_to_utc(row.get("event_datetime_utc", ""))

                normalized_data.append(
                    {
                        "event_id": f"{sport.value}_{row.get('source_event_id')}",
                        "sport": sport.value,
                        "league": league,
                        "season": str(row.get("season", "")),
                        "event_datetime_utc": dt.isoformat(),
                        "home_team": home_team,
                        "away_team": away_team,
                        "status": row.get("status", "UNKNOWN"),
                        "venue": row.get("venue"),
                        "source": provider.provider_name,
                        "source_event_id": str(row.get("source_event_id", "")),
                    }
                )
            except Exception as e:
                normalization_issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="various",
                        issue_type="normalization_error",
                        message=str(e),
                        record_id=str(row.get("source_event_id", idx)),
                    )
                )

        # 3. Validate
        req_val = RequiredFieldsValidator(
            ["event_id", "sport", "home_team", "away_team", "event_datetime_utc"]
        )
        uniq_val = UniqueEventValidator(id_field="event_id")

        v_data, req_issues = req_val.validate(normalized_data)
        v_data, uniq_issues = uniq_val.validate(v_data)

        all_issues = normalization_issues + req_issues + uniq_issues

        # 4. Enforce schema
        final_canonical = []
        for item in v_data:
            try:
                rec = CanonicalEventRecord(**item)
                final_canonical.append(rec.model_dump())
            except Exception as e:
                all_issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="schema",
                        issue_type="schema_coercion_error",
                        message=str(e),
                        record_id=item.get("event_id", "unknown"),
                    )
                )

        # 5. Write Processed
        proc_path = get_processed_storage_path("fixtures", sport, ingest_id)
        DataWriter.write_json(final_canonical, proc_path, f"{ingest_id}_processed.json")

        # 6. Generate Manifest
        manifest = IngestManifestRecord(
            ingest_id=ingest_id,
            run_timestamp_utc=datetime.now(timezone.utc),
            provider=provider.provider_name,
            sport=sport,
            dataset_type="fixtures",
            source_path=str(raw_path),
            output_path=str(proc_path),
            record_count=len(raw_data),
            valid_count=len(final_canonical),
            invalid_count=len(raw_data) - len(final_canonical),
            duplicate_count=len(uniq_issues),
            warning_count=0,
            issues=all_issues,
        )
        DataWriter.write_manifest(manifest, get_manifest_storage_path())
        return manifest

    def ingest_odds(
        self, provider: BaseOddsProvider, sport: SportType
    ) -> IngestManifestRecord:
        ingest_id = self._generate_ingest_id()
        logger.info(
            f"Starting odds ingestion {ingest_id} for {sport.value} via {provider.provider_name}"
        )

        raw_data = provider.fetch_odds(sport)
        raw_path = get_raw_storage_path(provider.provider_name, sport, "odds")
        DataWriter.write_json(raw_data, raw_path, f"{ingest_id}_raw.json")

        normalized_data = []
        normalization_issues = []
        for idx, row in enumerate(raw_data):
            try:
                dt = parse_datetime_to_utc(row.get("snapshot_ts_utc", ""))
                m_type = normalize_market_name(row.get("market_type", ""))

                # Basic handicap line parse
                hline = row.get("handicap_line")
                hline_val = float(hline) if hline and str(hline).strip() else None
                tline = row.get("total_line")
                tline_val = float(tline) if tline and str(tline).strip() else None

                normalized_data.append(
                    {
                        "event_id": f"{sport.value}_{row.get('source_event_id')}",
                        "market_type": m_type.value,
                        "bookmaker": str(row.get("bookmaker", provider.provider_name)),
                        "snapshot_ts_utc": dt.isoformat(),
                        "selection": str(row.get("selection", "")),
                        "decimal_odds": float(row.get("decimal_odds", 0.0)),
                        "implied_probability": (
                            float(row.get("implied_probability", 0.0))
                            if row.get("implied_probability")
                            else 0.0
                        ),
                        "handicap_line": hline_val,
                        "total_line": tline_val,
                        "raw_payload_metadata": {},
                    }
                )
            except Exception as e:
                normalization_issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="various",
                        issue_type="normalization_error",
                        message=str(e),
                        record_id=str(row.get("source_event_id", idx)),
                    )
                )

        req_val = RequiredFieldsValidator(
            ["event_id", "market_type", "bookmaker", "selection"]
        )
        odds_val = OddsSanityValidator()

        v_data, req_issues = req_val.validate(normalized_data)
        v_data, odds_issues = odds_val.validate(v_data)

        all_issues = normalization_issues + req_issues + odds_issues

        final_canonical = []
        for item in v_data:
            try:
                rec = CanonicalOddsRecord(**item)
                final_canonical.append(rec.model_dump())
            except Exception as e:
                all_issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="schema",
                        issue_type="schema_coercion_error",
                        message=str(e),
                        record_id=item.get("event_id", "unknown"),
                    )
                )

        proc_path = get_processed_storage_path("odds", sport, ingest_id)
        DataWriter.write_json(final_canonical, proc_path, f"{ingest_id}_processed.json")

        manifest = IngestManifestRecord(
            ingest_id=ingest_id,
            run_timestamp_utc=datetime.now(timezone.utc),
            provider=provider.provider_name,
            sport=sport,
            dataset_type="odds",
            source_path=str(raw_path),
            output_path=str(proc_path),
            record_count=len(raw_data),
            valid_count=len(final_canonical),
            invalid_count=len(raw_data) - len(final_canonical),
            duplicate_count=0,
            warning_count=0,
            issues=all_issues,
        )
        DataWriter.write_manifest(manifest, get_manifest_storage_path())
        return manifest

    def ingest_stats(
        self, provider: BaseStatsProvider, sport: SportType
    ) -> IngestManifestRecord:
        ingest_id = self._generate_ingest_id()
        logger.info(
            f"Starting stats ingestion {ingest_id} for {sport.value} via {provider.provider_name}"
        )

        raw_data = provider.fetch_team_stats(sport)
        raw_path = get_raw_storage_path(provider.provider_name, sport, "stats")
        DataWriter.write_json(raw_data, raw_path, f"{ingest_id}_raw.json")

        normalized_data = []
        normalization_issues = []
        for idx, row in enumerate(raw_data):
            try:
                league = normalize_league_name(row.get("league", "unknown"))
                team_name = self._resolve_team(
                    row.get("team_name", row.get("team_id", "")), sport.value, league
                )

                normalized_data.append(
                    {
                        "team_id": str(row.get("team_id", "")),
                        "team_name": team_name,
                        "sport": sport.value,
                        "league": league,
                        "season": str(row.get("season", "")),
                        "rating": (
                            float(row.get("rating", 0.0)) if row.get("rating") else None
                        ),
                        "recent_form": (
                            float(row.get("recent_form", 0.0))
                            if row.get("recent_form")
                            else None
                        ),
                        "rest_days": (
                            int(row.get("rest_days", 0))
                            if row.get("rest_days")
                            else None
                        ),
                        "rolling_metrics": {},
                    }
                )
            except Exception as e:
                normalization_issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="various",
                        issue_type="normalization_error",
                        message=str(e),
                        record_id=str(row.get("team_id", idx)),
                    )
                )

        req_val = RequiredFieldsValidator(["team_id", "team_name", "sport", "league"])
        v_data, req_issues = req_val.validate(normalized_data)

        all_issues = normalization_issues + req_issues

        final_canonical = []
        for item in v_data:
            try:
                rec = CanonicalTeamStatsRecord(**item)
                final_canonical.append(rec.model_dump())
            except Exception as e:
                all_issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="schema",
                        issue_type="schema_coercion_error",
                        message=str(e),
                        record_id=item.get("team_id", "unknown"),
                    )
                )

        proc_path = get_processed_storage_path("stats", sport, ingest_id)
        DataWriter.write_json(final_canonical, proc_path, f"{ingest_id}_processed.json")

        manifest = IngestManifestRecord(
            ingest_id=ingest_id,
            run_timestamp_utc=datetime.now(timezone.utc),
            provider=provider.provider_name,
            sport=sport,
            dataset_type="stats",
            source_path=str(raw_path),
            output_path=str(proc_path),
            record_count=len(raw_data),
            valid_count=len(final_canonical),
            invalid_count=len(raw_data) - len(final_canonical),
            duplicate_count=0,
            warning_count=0,
            issues=all_issues,
        )
        DataWriter.write_manifest(manifest, get_manifest_storage_path())
        return manifest
