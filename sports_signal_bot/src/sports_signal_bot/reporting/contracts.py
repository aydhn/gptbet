from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MetricDefinitionRecord(BaseModel):
    metric_name: str
    metric_family: str
    description: str
    unit: str
    directionality: str
    aggregation_method: str
    source_components: List[str] = Field(default_factory=list)
    required_inputs: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)
    audience_tags: List[str] = Field(default_factory=list)
    schema_version: str = "1.0"


class MetricLineageRecord(BaseModel):
    source_manifests: List[str]
    input_summaries: List[str]
    aggregation_method: str
    time_range_start: datetime
    time_range_end: datetime
    included_filters: Dict[str, Any]
    normalization_notes: str
    is_mixed_sample: bool
    freshness_timestamp: datetime


class MetricValueRecord(BaseModel):
    metric_name: str
    value: float
    unit: str
    lineage: Optional[MetricLineageRecord] = None


class KPIDefinitionRecord(BaseModel):
    kpi_id: str
    name: str
    family: str
    description: str
    unit: str
    directionality: str
    aggregation_method: str
    source_components: List[str]
    caveats: List[str] = Field(default_factory=list)


class KPIValueRecord(BaseModel):
    kpi_id: str
    value: float
    unit: str
    lineage: Optional[MetricLineageRecord] = None


class ReportingUniverseRecord(BaseModel):
    universe_id: str
    description: str
    filters: Dict[str, Any]
    event_count: int


class ReportSectionRecord(BaseModel):
    section_name: str
    audience: str
    primary_metrics: List[MetricValueRecord] = Field(default_factory=list)
    supporting_metrics: List[MetricValueRecord] = Field(default_factory=list)
    narrative_summary: str = ""
    caveats: List[str] = Field(default_factory=list)
    referenced_artifacts: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    links_to_deeper_docs: Optional[List[str]] = None


class KPIBundleRecord(BaseModel):
    kpis: List[KPIValueRecord]


class MetricComparisonRecord(BaseModel):
    metric_name: str
    current_value: float
    previous_value: float
    delta_abs: float
    delta_pct: float
    classification: str


class ExecutiveSummaryRecord(BaseModel):
    overall_status: str
    top_kpis: KPIBundleRecord
    key_wins: List[str]
    key_risks: List[str]
    operational_health: str
    release_governance_highlights: str
    immediate_attention_items: List[str]


class TechnicalSummaryRecord(BaseModel):
    sections: List[ReportSectionRecord]


class ReportBundleRecord(BaseModel):
    reporting_period: str
    time_range_start: datetime
    time_range_end: datetime
    included_sports_markets: List[str]
    included_runs_artifacts: List[str]
    sample_universe_summary: ReportingUniverseRecord
    audience_profile: str
    sections: List[ReportSectionRecord]
    kpi_bundle: KPIBundleRecord
    notable_events: List[str]
    warnings_caveats: List[str]


class PeriodSummaryRecordV2(BaseModel):
    bundle: ReportBundleRecord


class ReportingManifest(BaseModel):
    manifest_id: str
    created_at: datetime
    bundle: ReportBundleRecord


class AudienceProfileRecord(BaseModel):
    name: str
    description: str
    sections: List[str]
    detail_level: str
    include_diagnostics: bool
    focus_kpis: List[str]
    tone: str
