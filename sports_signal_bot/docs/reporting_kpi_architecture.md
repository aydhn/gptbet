---
owner_role: lead_engineer
doc_family: architecture
freshness_window_days: 90
last_reviewed: 2026-04-28
---

# Unified Reporting and KPI Architecture

## Why Unified Metrics/Reporting Now?
The platform has grown to produce a variety of metrics across evaluation, inference, and operational health. This unified reporting architecture centralizes metric governance, definition, and audience-aware reporting to prevent fragmented dashboards and inconsistent KPI meanings.

## KPI Taxonomy
KPIs are defined centrally in `configs/reporting/kpis.yaml`. They are categorized into families such as:
- `predictive_quality_metrics`
- `operational_health_metrics`
- `release_governance_metrics`

Each KPI has a strict definition, target directionality (e.g., `higher_is_better`), and a required aggregation method.

## Audience Profiles
Reporting is strictly audience-aware, controlled by `configs/reporting/audiences.yaml`:
- **Executive**: High-level, KPI-focused, concise tone.
- **Operator**: Operational, incident-aware, standard tone.
- **Maintainer**: Highly technical, diagnostic-rich, full lineage provided.

## Metric Lineage
All computed metrics generate a `MetricLineageRecord` indicating:
- Source artifacts/manifests
- Aggregation methodology
- Exact time range
- `is_mixed_sample` flag to warn against comparing metrics from different universes.

## Reporting Outputs
The system generates:
- JSON Data Bundle (`report_bundle.json`)
- Markdown Executive/Technical Summary (`report_bundle.md`)
- CSV Extract for KPIs (`kpi_values.csv`)
- System Manifest (`reporting_manifest.json`)
