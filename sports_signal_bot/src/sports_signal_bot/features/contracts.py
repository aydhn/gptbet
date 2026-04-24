from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class NullPolicy(str, Enum):
    KEEP_NULLS = "keep_nulls"
    FILL_DEFAULTS = "fill_defaults"
    ADD_MISSING_INDICATORS = "add_missing_indicators"

class FeatureBuildContext(BaseModel):
    sport: str
    market_type: Optional[str] = None
    event_time_cutoff_policy: str = "strict_pre_match"
    lookback_windows: List[int] = [3, 5, 10]
    line_values: Optional[Dict[str, float]] = None
    provider_filters: Optional[List[str]] = None
    include_feature_families: Optional[List[str]] = None
    exclude_feature_families: Optional[List[str]] = None
    null_policy: NullPolicy = NullPolicy.KEEP_NULLS
    seed: int = 42
    run_id: str

class FeatureMatrixRecord(BaseModel):
    event_id: str
    sport: str
    league: str
    event_datetime_utc: str
    feature_version: str
    feature_build_run_id: str
    features: Dict[str, Any]

class FeatureManifestRecord(BaseModel):
    run_id: str
    built_at_utc: str
    sport: str
    market_type: Optional[str] = None
    source_datasets: List[str]
    source_record_counts: Dict[str, int]
    selected_builders: List[str]
    produced_columns: List[str]
    null_summary: Dict[str, int]
    row_count: int
    output_path: str
    warnings: List[str] = Field(default_factory=list)

class FeatureAvailabilitySummary(BaseModel):
    run_id: str
    builder_column_counts: Dict[str, int]
    missing_sources: List[str] = Field(default_factory=list)
    skipped_builders: List[str] = Field(default_factory=list)
