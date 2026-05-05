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

## Evidence Atlas & Narrative Federations (Phase 92)

The **Evidence Atlas** layer establishes a sovereign evidence topography combining multiple narratives into structured **Narrative Compiler Federations**, bounding exchanges into **Assurance Exchange Meshes**, and mediating disputes through **Replay Clearing Councils**. The overall **Sovereign Governance Evidence Atlas** integrates these into navigable, transparent, and sovereignty-preserving structures.

* **Usage**:
  * Run a full evidence atlas pass: `python -m sports_signal_bot.main evidence-atlas run-evidence-atlas-pass`

## Phase 94: Sovereign Governance Trace Routing

Phase 94 introduces the `trace_routing` katmanı.

The **Trace Routing Katmanı** aims to provide boundary and linkage across various proof catalogs, observatory exchanges, integrity councils and overall governance trace routes.

### Components
- **Proof Catalog Federations**: Links individual catalogs with currentness and lineage tracking without acting as a single runtime authority.
- **Observatory Signal Exchanges**: Uses bounded signal exchange, preventing scope widening and ensuring caveats are not dropped.
- **Narrative Integrity Councils**: Resolves integrity disputes over evidence gaps, preventing raw overrides of local sovereignty.
- **Sovereign Governance Trace Routers**: Routes drilldowns and traces while preserving caveats and explicitly capturing No-Safe recovery hints.

### Key Commands

```bash
python -m sports_signal_bot.main trace-routing run-trace-routing-pass
python -m sports_signal_bot.main trace-routing preview-proof-federations
```

### Safety & Sovereignty Principles
- Federated proofs, exchanged signals, and trace routes remain bounded and non-authoritative.

## Phase 95: Sovereign Governance Context Assembly
This phase implements trace router federations, proof freshness councils, observatory exchange boards, and sovereign governance context assemblers. It ensures that trace paths, proof freshness, and signal exchanges are aggregated into explainable, non-authoritative context bundles that strictly preserve caveats, local deny sovereignty, and no-safe recovery hints.

## Phase 96: Coherence Scoring

The coherence scoring layer builds upon trace routing and context assembly to provide explainable, federated context evaluations. It introduces:

- **Context Assembler Federations**: Groups context assemblers into bounded, non-authoritative federations.
- **Freshness Dispute Chambers**: Structure to evaluate, decay, and rule on freshness disputes.
- **Trace Evidence Brokers**: Match and route traces within constraints without widening scope.
- **Sovereign Governance Coherence Scorers**: Measure internal consistency to produce bounded, explainable scores.

**Commands:**
- `python -m sports_signal_bot.main coherence-scoring run-coherence-scoring-pass`
- `python -m sports_signal_bot.main coherence-scoring list-coherence-scoring-strategies`

**Design Principles:**
Coherence outputs remain strictly bounded. Freshness gaps, evidence sufficiency limits, and any `no_safe_recovery_hint` will cap the coherence score, ensuring that missing evidence or stale context prevents false assurance from being published. Caveats and sovereignty rules are strictly preserved in federated outputs.

## Phase 97: Sovereign Governance Alignment Compilers

The Alignment Compilers layer aims to bring together coherence scorer federations, context dispute tribunals, and evidence broker exchanges into non-authoritative sovereign governance alignment outputs.

Key differences:
- **Coherence Federation**: Combines scores without overriding them, capturing penalties and staleness.
- **Context Dispute Tribunal**: Processes context disputes with bounded replay reviews and evidence freshness.
- **Evidence Broker Exchange**: Shares evidence without scope widening and preserves caveats.
- **Governance Alignment Compiler**: Derives bounded, explainable alignment bands while preserving no-safe visibility and local sovereignty.

**Commands:**
- `python -m sports_signal_bot.main alignment-compilers run-alignment-compilers-pass`
- `python -m sports_signal_bot.main alignment-compilers list-alignment-compiler-strategies`

**Safety & Sovereignty Principles:**
- Alignment outputs, federated coherence, tribunal decisions, and broker exchanges remain bounded and non-authoritative.
- Freshness, evidence sufficiency, and no-safe visibility dominate alignment quality.
- Any freshness gap or missing evidence results in caps (e.g., `review_only_alignment`).
