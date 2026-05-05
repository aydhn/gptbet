# Reviewer Guide: Freshness, Evidence, & Coherence Integrity

Reviewers must inspect `FreshnessDisputeCaseRecord` and `EvidenceBrokerMatchRecord` outputs.

Look out for cases where evidence completeness is partial but the outcome mistakenly suggests a strong bounded trace.
Coherence scoring relies on preserving `no_safe_visibility`. If a reviewer sees an aggregated context omitting this hint, it's a critical safety violation.
