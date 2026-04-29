---
owner_role: maintainer
doc_family: reference
freshness_window_days: 90
last_reviewed: 2026-04-28
---

# Report Bundle Data Structure Guide

## Overview
A `ReportBundleRecord` is the definitive single source of truth for a reporting period. It encapsulates the computed metrics, KPIs, audience details, and underlying data lineage.

## Bundle Components
- **Reporting Period & Range**: Contextual time data.
- **Sample Universe Summary**: Defines the events/filters the report covers. Crucial for detecting mixed-universe comparisons.
- **Sections**: Narratives and metrics filtered and styled according to the target audience profile.
- **KPI Bundle**: The strict subset of metrics defined as Key Performance Indicators.
- **Warnings & Caveats**: Any system-generated warnings, e.g., missing data, mixed universes, or significant metric degradations.

## Artifact Manifest
Every reporting run generates a `ReportingManifest` (saved as `reporting_manifest.json`), which attaches a unique ID and creation timestamp to the bundle, ensuring exact point-in-time auditability.
