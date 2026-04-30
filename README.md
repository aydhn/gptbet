# Sports Signal Bot
## Phase 42: Feedback Assimilation & Learning Architecture

This architecture introduces a controlled, scoped, and human-in-the-loop learning layer on top of the adjudication memory. It avoids silent, black-box auto-modifications in favor of explicit, evidence-backed tuning suggestions.

### Precedent to Suggestion Flow
1. **Feedback Aggregation**: Adjudication records, precedents, and corrections are aggregated by target component (e.g. `provider_trust`, `threshold`).
2. **Pattern Mining**: Common elements across feedback signals are mined to create `PatternCandidateRecord`s.
3. **Structured Suggestion**: Candidates are mapped into a structured DSL containing condition/action blocks.
4. **Scoring & Safety**:
    - **Support**: Evaluated based on case counts and contradiction burdens.
    - **Confidence**: Scored into bands (e.g., `high`, `medium`, `unsafe_to_apply`).
    - **Risk**: Classified (e.g., `low`, `critical`) based on downstream blast radius and component criticality.
    - **Scope**: Evaluated for safety; overly broad changes are narrowed or prohibited.
5. **Assimilation Decision**: Based on the scores, the system assigns a recommendation mode:
    - `advisory_only`
    - `candidate_patch`
    - `manual_review_required`
    - `blocked`

### Why Not Automatic Self-Modification?
The system adheres to the principle "No Silent Self-Modification". Direct rule rewrites based on limited feedback carry significant risk (e.g., threshold drifts causing large-scale failures). Instead, we generate *advisory* or *test-gated candidate patches* that require manual review or automated simulation quality gates before being deployed.

### Learning Passes
Run the assimilation engine via:
`python -m sports_signal_bot.main learning run-learning-pass`
`python -m sports_signal_bot.main learning preview-pattern-candidates`
`python -m sports_signal_bot.main learning preview-tuning-suggestions`
`python -m sports_signal_bot.main learning list-learning-strategies`

For more details, see the documentation in `docs/`.

## Phase 43: Suggestion Sandbox Architecture
The Suggestion Sandbox provides an isolated, highly-controlled laboratory to safely evaluate candidate patch suggestions before they impact the active system state.

- **Candidate Patches**: Suggestions are converted into scoped, transient configuration overrides.
- **Before-After Simulations**: Enforces a strict same-universe comparison between the baseline and the proposed variant.
- **Commands**: Use `python -m sports_signal_bot.main simulate-suggestion --suggestion-id <id>` to run a simulation and `python -m sports_signal_bot.main list-simulation-strategies` to view available simulation methodologies.
- **Safety**: Simulations are deterministic, strictly isolated from production data stores, and generate automated risk recommendations for operators and reviewers.

## Phase 44: Batch Candidate Tournaments
The Batch Candidate Tournament architecture provides a multi-objective ranking system to safely compare multiple patches within the same comparison universe. It introduces pareto-front analysis, safety lanes, and shortlist recommendations without auto-promoting patches.

- **Commands**:
  - `python -m sports_signal_bot.main tournaments run-tournament --family threshold_tournament`
  - `python -m sports_signal_bot.main tournaments preview-shortlist --tournament-id <id>`
- **Safety**: Generates explicit lanes (safe, advisory, exploratory) and prevents auto-deployments. It acts as a decision-support layer for human reviewers.
- **Documentation**: See `docs/candidate_tournament_architecture.md` for more details.
