---
owner: ecosystem_sync_team
family: architecture
freshness_window_days: 90
---

# Discovery Subscriptions & Ecosystem Sync Architecture

This document describes the Phase 66 architecture for continuous ecosystem synchronization.

## Overview
The Ecosystem Sync layer moves the system from static discovery catalogs to a continuous feed bus, leveraging discovery subscriptions, federated catalog overlays, and trust-weighted routing.

## Components
1. **Discovery Subscriptions**: Policy-driven watch channels for external catalogs. Subscriptions track freshness, lag, and quarantine status without automatically trusting fetched content.
2. **Catalog Overlays**: Merges updates from multiple subscription sources into unified overlays while strictly preserving data lineage and tracking freshness/trust conflicts.
3. **Supersession Propagation**: Ensures that updates to current entries correctly tombstone old versions and propagate new references throughout the routing cache.
4. **Ecosystem Routing**: A trust-weighted routing engine that scores discovery candidates based on trust, freshness, compatibility, and replay readiness.

## Integration
This layer bridges Phase 65's Discovery Catalogs and Phase 64's Capability Negotiation, creating a continuous feedback loop where new sources are discovered, subscribed to, and routed securely based on active health checks.
