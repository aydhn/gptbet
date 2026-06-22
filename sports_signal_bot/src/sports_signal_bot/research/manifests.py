import datetime
from typing import Any, Dict, List

from sports_signal_bot.research.contracts import (PeriodRunRecord,
                                                  ResearchRunManifest,
                                                  ResearchScenario)


def build_research_manifest(
    run_id: str,
    scenario: ResearchScenario,
    period_records: List[PeriodRunRecord],
    aggregate_paths: Dict[str, str],
    config_snapshot: Dict[str, Any],
) -> ResearchRunManifest:
    """Builds the final research manifest."""

    completed = sum(1 for p in period_records if p.status == "success")
    skipped = sum(1 for p in period_records if p.status == "skipped")

    families = set()
    warnings = []

    for p in period_records:
        families.update(p.retrained_model_names)
        families.update(p.reused_model_names)
        if p.ensemble_refresh_status != "not_applicable":
            families.add("ensemble")
        if p.stacker_refresh_status != "not_applicable":
            families.add("stacker")

        if p.warnings:
            prefix = f"Period {p.period_id}: "
            warnings.extend(prefix + w for w in p.warnings)

    return ResearchRunManifest(
        run_id=run_id,
        run_timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scenario=scenario,
        total_periods=len(period_records),
        completed_periods=completed,
        skipped_periods=skipped,
        source_families_involved=list(families),
        aggregate_summary_paths=aggregate_paths,
        warnings=warnings,
        config_snapshot=config_snapshot,
    )
