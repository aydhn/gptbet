# Simulation Recommendation Taxonomy

- **REJECT_PATCH**: Degraded performance. Do not proceed.
- **KEEP_ADVISORY_ONLY**: Minor/Trivial changes. Not worth the patch rollout cost.
- **REQUEST_MORE_DATA**: Inconclusive or mixed results on small samples.
- **SAFE_FOR_REVIEW**: Significant material change, safe to move to human review.
- **SAFE_FOR_CANDIDATE_RELEASE_PATH**: Consistent improvement, safe for automated deployment pipelines.
- **NARROW_SCOPE_AND_RETRY**: High impact but broad scope. Needs narrowing.
- **CONFLICTING_EVIDENCE**: Evidence trails contradict simulation outputs.
