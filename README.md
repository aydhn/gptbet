# Sports Signal Bot

Phase 40: Evidence & Explainability Layer

The system includes a dedicated layer to translate actions (approvals, blocks, signal scores) into deterministic, auditable evidence bundles.

## Key Features
- **Evidence Bundles**: Combines claims, citations, and lineage.
- **Why / Why-Not**: Explicitly answers why a decision was reached, or why it wasn't.
- **Counterfactual Hints**: Provides non-executable suggestions on what would have changed a decision (e.g., lower threshold).
- **Lineage Tracing**: Follow a decision back to its raw provider data.

## Useful Commands
- `python -m sports_signal_bot.main evidence build-evidence-bundles`
- `python -m sports_signal_bot.main evidence explain-decision <event_id>`
- `python -m sports_signal_bot.main evidence explain-why-not <event_id>`
