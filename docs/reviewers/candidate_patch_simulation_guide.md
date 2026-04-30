# Reviewer Guide: Candidate Patch Simulations

When reviewing a candidate patch, you must evaluate the simulation outputs.

## Key Checks
- **Same Universe Validation**: Ensure the baseline and variant used identical input samples.
- **Materiality**: Review the materiality band (Trivial to Critical) to understand impact scale.
- **Recommendations**: If a simulation recommends `safe_for_review`, verify the metrics. If it's `mixed` or `degraded`, proceed with extreme caution or reject.
- **Scope Limits**: High-risk patches must be narrowly scoped.
