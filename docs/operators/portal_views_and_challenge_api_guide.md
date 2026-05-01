# Portal Views & Challenge API Guide for Operators

## Portal Views
Operators should be familiar with the various views exposed through the Verifier Portal. These include:
- `publication_index_view`
- `disclosure_bundle_view`
- `checkpoint_summary_view`
- `challenge_status_view`

These views are strictly profile-aware. Public viewers receive the minimum necessary detail, whereas auditors receive deep proof-linked decisions.

## Managing Challenge APIs
The Challenge API is the intake mechanism for external queries and challenges. It employs a "quarantine-first" model. Unknown or malformed submissions are automatically placed into quarantine.
- Run `python -m sports_signal_bot.main verifier-portal preview-challenge-api-submissions` to review recent submissions.

## Guardrails
Operators should actively monitor portal diagnostics. Crucial guardrails ensure:
- Stale feeds cannot be marked as current.
- Internal details do not leak into public-safe packets.
- Suspicious challenge payloads are stripped.
