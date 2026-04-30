---
owner_role: "evidence_engineering"
doc_family: "reference"
freshness_days: 90
---

# Evidence Claim Taxonomy

Claims in the Evidence system categorize findings.

- `data_origin_claim`: Where the data came from.
- `data_quality_claim`: Warnings about quality (stale, partial).
- `prediction_claim`: What a model/calibrator asserted.
- `policy_claim`: What rules blocked or allowed a trade.

Status levels range from `supported` to `contradicted`. Strength ranges from `high` to `low`.
