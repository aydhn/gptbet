
### Evidence Atlas & Narrative Federations (Phase 92)

The **Evidence Atlas** layer establishes a sovereign evidence topography combining multiple narratives into structured **Narrative Compiler Federations**, bounding exchanges into **Assurance Exchange Meshes**, and mediating disputes through **Replay Clearing Councils**. The overall **Sovereign Governance Evidence Atlas** integrates these into navigable, transparent, and sovereignty-preserving structures.

* **Narrative Federations, Assurance Meshes, and Evidence Atlases:**
  * Unlike singular narrative generation, Federations compile, overlay freshness constraints, and preserve caveats across outputs.
  * Meshes provide bounded paths for transmitting assurance, dynamically degrading when under pressure without losing no-safe visibility.
  * Clearing Councils evaluate bounded match conditions with strict quorum and precedence rules to resolve replay clearing conflicts safely.
  * Evidence Atlases create non-authoritative (but verifiable) navigation overlays, linking debt, staleness, caveat constraints, and sovereignty rules across the governance map.

* **Usage**:
  * Run a full evidence atlas pass: `python -m sports_signal_bot.main evidence-atlas run-evidence-atlas-pass`
  * Preview federations and meshes: `python -m sports_signal_bot.main evidence-atlas preview-narrative-federations`
  * Check overall evidence atlas health: `python -m sports_signal_bot.main evidence-atlas preview-evidence-atlas-health`

* **Why Federated Assurance Remains Bounded**:
  Federated output explicitly cannot create new runtime authority; it merely navigates and synthesizes existing caveats, capping its strength by the weakest or stalest link to ensure safety.

* **Why Freshness, Evidence, and No-Safe Visibility Dominate**:
  An evidence atlas without strict freshness boundaries acts as a false map. Stale edges and unresolved conflicts force paths to downgrade (to `review_only` or `caveated`), and any `no_safe_recovery_hint` is strictly preserved to prevent executive summarization from hiding critical localized failures.
# Sports Signal Bot

(Omitted unchanged sections...)

## Assurance Exchange Architecture (Phase 91)
The assurance exchange layer provides visibility into the governance and resilience of the system by coordinating bounded, truth-preserving artifacts.

It includes:
- **Dashboard Exchanges**: For sharing assurance outputs, not authority.
- **Federation Boards**: For deliberation and cap enforcement.
- **Replay Clearing Layers**: For matching offers and requests bounded by evidence.
- **Narrative Compilers**: For producing honest, caveat-preserving summaries tailored to distinct audiences.

**Commands:**
- `python -m sports_signal_bot.main assurance-exchange run-assurance-exchange-pass`

**Design Principles:**
Exchanged assurance and narratives remain bounded and non-authoritative. Debt aging, replay evidence, and no-safe visibility consistently dominate assurance quality, preventing overly polished or deceitful executive summaries.

## Assurance Exchange Architecture (Phase 91)
The assurance exchange layer provides visibility into the governance and resilience of the system by coordinating bounded, truth-preserving artifacts.

It includes:
- **Dashboard Exchanges**: For sharing assurance outputs, not authority.
- **Federation Boards**: For deliberation and cap enforcement.
- **Replay Clearing Layers**: For matching offers and requests bounded by evidence.
- **Narrative Compilers**: For producing honest, caveat-preserving summaries tailored to distinct audiences.

**Commands:**
- `python -m sports_signal_bot.main assurance-exchange run-assurance-exchange-pass`

**Design Principles:**
Exchanged assurance and narratives remain bounded and non-authoritative. Debt aging, replay evidence, and no-safe visibility consistently dominate assurance quality, preventing overly polished or deceitful executive summaries.
