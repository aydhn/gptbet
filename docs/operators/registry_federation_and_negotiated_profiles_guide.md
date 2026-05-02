---
owner: "@principal_assurance_engineer"
family: "operator_guide"
freshness_window: "90d"
---

# Registry Federation & Negotiated Profiles Guide

## Introduction
This guide is for operators managing the federation of external verifiers and partner registries. It covers how to use capability negotiation to establish safe, interoperable bridges.

## Key Principles
- **Federation means verified compatibility, not blind trust.** We do not blindly trust foreign registries; we negotiate a safe subset of capabilities.
- **Profiles Expire.** Negotiated profiles become stale and must be renegotiated.
- **Drift is Expected.** External verifiers may drop or add support over time. The system will detect this capability drift and force renegotiation or quarantine.

## Managing Onboarding
When an external verifier attempts to join the federation, they submit a `CapabilityProfileRecord`. The system evaluates it against our `FederationPolicyRecord`.
- If compatible, they are accepted.
- If unsupported proofs or unknown specs are detected, they are quarantined for manual review.

## Managing Drift
Monitor the drift reports. If a partner registry drops support for our proof formats, the negotiated profile will be invalidated.
