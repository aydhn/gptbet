# Registry Currentness & Policy Pack Guide

As an operator, you'll manage the lifecycle of entries in the Corridor Registry.

## Managing Currentness
- **Stale Entries:** Watch the `freshness_state`. If it's stale, the entry is no longer considered current.
- **Supersession:** When a new corridor or treaty supersedes an old one, use the `supersede_registry_entry` function to preserve the lineage.
- **Health:** Review `registry_health_contribution` to see if your registry has too many stale or superseded current pointers.

## Working with Conformance Packs
- Packs list `required_dimensions` and track `satisfied_dimensions` vs `missing_dimensions`.
- Ensure you have the necessary `ConformancePackEvidenceRecord` pointers available to satisfy blocking gaps.
