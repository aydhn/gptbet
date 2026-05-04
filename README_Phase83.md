# Phase 83: Governance Tier Councils & Sovereign Projection Audit Exchanges

This phase introduces a robust **Governance Fabric** layer that sits on top of the overlay meshes, multi-tier routes, and baseline registries. It shifts the system from generating simple bounded hints to executing governed consensus, carrying consortium signals through managed fabrics, federating baseline currentness safely, and auditing projection exchanges.

## Core Concepts

*   **Governance Tier Councils:** Model bounded governance adjudication. Councils interpret conflict and route pressure. They *do not* execute runtime authority; instead, they produce bounded governance hints, downgrades, suppressions, and review mandates.
*   **Consortium Signal Fabrics:** Carry signals across the ecosystem within bounded, strict channels. They manage provenance, freshness decay, corroboration, and suppression. They prevent signal scope broadening and drop/suppress inputs during stale or conflicting bursts.
*   **Baseline Registry Federation:** Projects baseline currentness, supersession, and applicability across linked registries. Importantly, federated pointers *do not* override local currentness but serve as bounded hint bases.
*   **Sovereign Projection Audit Exchanges:** Package exactly how a projection was made (inputs, caveats, baselines) along with verifiable evidence. They allow external controllers to replay the projection and apply caps or downgrades if the audit packet is missing evidence or mismatches during replay.

## Key CLI Commands

*   `python -m sports_signal_bot.main governance-fabric run-governance-fabric-pass`
*   `python -m sports_signal_bot.main governance-fabric preview-governance-councils`
*   `python -m sports_signal_bot.main governance-fabric preview-signal-fabrics`
*   `python -m sports_signal_bot.main governance-fabric preview-baseline-federations`
*   `python -m sports_signal_bot.main governance-fabric preview-projection-audit-exchanges`

## Guardrails Enforced
*   Council decisions act as upper-tier blocks/hints, never bypassing local sovereignty denies.
*   Consortium fabric flow strictly prevents scope broadening.
*   Stale federated baselines cap projection strength (no strong hints from stale data).
*   Audit packets without evidence references are blocked.
*   Audit replay mismatches result in immediate projection caps/downgrades by the controller.
