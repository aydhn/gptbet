from enum import Enum

class ControllerState(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    REFRESH_PENDING = "refresh_pending"
    REFRESHING = "refreshing"
    REFRESHED = "refreshed"
    FROZEN = "frozen"
    BLOCKED = "blocked"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    FAILED_REFRESH = "failed_refresh"
    SAFE_FALLBACK_ACTIVE = "safe_fallback_active"

class RefreshRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ProblemClass(str, Enum):
    DATA_FRESHNESS = "data_freshness"
    ARTIFACT_FRESHNESS = "artifact_freshness"
    RUNTIME_PIPELINE = "runtime_pipeline"
    DISPATCH_OPS = "dispatch_ops"
    RISK_STATE = "risk_state"

class RefreshActionFamily(str, Enum):
    # Low-risk auto actions
    CATALOG_REFRESH = "catalog_refresh"
    RERUN_ARTIFACT_RESOLUTION = "rerun_artifact_resolution"
    FALLBACK_CHAIN_PROMOTION = "fallback_chain_promotion"
    CACHE_INVALIDATION = "cache_invalidation"
    SNAPSHOT_RESELECTION = "snapshot_reselection"
    RELOAD_LATEST_STABLE_ARTIFACT = "reload_latest_stable_artifact"
    SWITCH_TO_STABLE_SLOT_POLICY = "switch_to_stable_slot_policy"
    ENABLE_SAFE_FALLBACK_MODE = "enable_safe_fallback_mode"

    # Medium-risk conditional actions
    REBUILD_FEATURES_FOR_INFERENCE = "rebuild_features_for_inference"
    RERUN_INFERENCE_STEP_SUBSET = "rerun_inference_step_subset"
    RERUN_DISPATCH_WITH_SAFE_MODE = "rerun_dispatch_with_safe_mode"
    REFRESH_SOURCE_METADATA = "refresh_source_metadata"
    REFRESH_REGIME_INPUTS = "refresh_regime_inputs"

    # High-risk / approval-required placeholder
    RETRAIN_MODEL = "retrain_model"
    RECALIBRATE_MODEL = "recalibrate_model"
    REBUILD_STACKER = "rebuild_stacker"
    RECOMPUTE_THRESHOLD_POLICY = "recompute_threshold_policy"
    RECOMPUTE_POLICY_ARTIFACT_FAMILY = "recompute_policy_artifact_family"
    REFRESH_SIZING_POLICY = "refresh_sizing_policy"
