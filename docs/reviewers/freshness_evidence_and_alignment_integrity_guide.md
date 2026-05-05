# Reviewer Guide: Freshness, Evidence, and Alignment Integrity

## What to Look For
When reviewing the outputs of the Alignment Compilers layer, auditors and reviewers must verify:

1. **Staleness is Penalized**: Check that any `stale` input to an alignment compiler correctly triggers a `stale_context_penalty` and prevents the generation of a `strong_bounded_alignment` band.
2. **Evidence Sufficiency is Enforced**: Ensure that tribunals applying caps or brokers routing exchanges degrade their outputs if evidence is marked `incomplete`.
3. **Caveat Preservation**: Verify that caveats present in raw context bundles or single coherence scores are visibly carried through to the final `preserved_caveats` list in the `AlignmentOutputRecord`.
4. **No-Safe Visibility**: Confirm that any `no_safe_recovery_hint` is explicitly retained. If the `no_safe_visibility_pass` fails, the final alignment must be heavily degraded (e.g., `review_only_alignment` or `critically_misaligned`).

## Anti-Patterns
- **Silently Dropping Caveats**: An alignment compiler output that looks "clean" but originated from heavily caveated inputs is a critical failure.
- **Overriding Local Deny**: If a context contains a local sovereignty failure, the alignment compiler must not output a "strong" alignment.
