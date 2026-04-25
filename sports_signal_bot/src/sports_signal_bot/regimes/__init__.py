from .contracts import (EventRegimeRecord, PeriodRegimeRecord,
                        RegimeAssignmentResult, RegimeCoverageRecord,
                        RegimeDefinition, RegimeEvaluationRecord,
                        RegimeManifest)
from .coverage import calculate_coverage
from .definitions import (BaseRegimeClassifier, RuleBasedEventRegimeClassifier,
                          RuleBasedPeriodRegimeClassifier)
from .factory import RegimeFactory
from .inputs import (EventRegimeInputs, PeriodRegimeInputs,
                     build_event_regime_inputs, build_period_regime_inputs,
                     merge_regime_supporting_features)
from .manifests import build_regime_manifest
from .registry import RegimeRegistry
from .reporting import (export_event_regimes_csv, export_period_regimes_csv,
                        export_regime_manifest, generate_regime_summary)
from .runner import RegimeRunner
from .thresholds import RegimeConfig, RegimeThresholdsConfig


# Integration point for evaluation
def evaluate_with_regime_filter(
    evaluation_func, records: list, regime_family: str, regime_label: str
) -> dict:
    filtered = [
        r
        for r in records
        if r.regime_family == regime_family and r.regime_label == regime_label
    ]
    return evaluation_func(filtered)


__all__ = [
    "RegimeDefinition",
    "EventRegimeRecord",
    "PeriodRegimeRecord",
    "RegimeAssignmentResult",
    "RegimeCoverageRecord",
    "RegimeEvaluationRecord",
    "RegimeManifest",
    "RegimeThresholdsConfig",
    "RegimeConfig",
    "EventRegimeInputs",
    "PeriodRegimeInputs",
    "build_event_regime_inputs",
    "build_period_regime_inputs",
    "merge_regime_supporting_features",
    "BaseRegimeClassifier",
    "RuleBasedEventRegimeClassifier",
    "RuleBasedPeriodRegimeClassifier",
    "RegimeRegistry",
    "RegimeFactory",
    "RegimeRunner",
    "calculate_coverage",
    "build_regime_manifest",
    "export_event_regimes_csv",
    "export_period_regimes_csv",
    "export_regime_manifest",
    "generate_regime_summary",
    "evaluate_with_regime_filter",
]
