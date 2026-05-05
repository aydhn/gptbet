# Maintenance: Coherence Scoring Runbook

If you see an alert for "coherence score strong band despite no_safe visibility failure":
1. Immediately check `preview-coherence-scorers`.
2. Trace the inputs causing the failure back to their specific `ContextFederationBundleRecord`.
3. Force a refresh using the corresponding context assembly commands, ensuring caveats and no-safe hints are restored.
