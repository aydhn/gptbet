import datetime
from typing import List

from sports_signal_bot.regimes.contracts import (RegimeCoverageRecord,
                                                 RegimeEvaluationRecord,
                                                 RegimeManifest)


def build_regime_manifest(
    run_id: str,
    active_families: List[str],
    coverages: List[RegimeCoverageRecord],
    evaluations: List[RegimeEvaluationRecord],
) -> RegimeManifest:
    warnings = []
    for c in coverages:
        if not c.minimum_rows_satisfied:
            warnings.append(f"Low sample for {c.regime_family}.{c.regime_label}")

    return RegimeManifest(
        run_id=run_id,
        timestamp=datetime.datetime.utcnow(),
        active_families=active_families,
        coverage_summaries=coverages,
        evaluation_summaries=evaluations,
        warnings=warnings,
    )
