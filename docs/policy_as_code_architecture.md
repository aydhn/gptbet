# Policy As Code Architecture

This document describes why federated governance needs Policy as Code and outlines the architecture of rule bundles, precedence, overlaps, reviews, and control plane integrations.

## Why Federated Governance Needs Policy as Code
Federated governance implies decentralized execution. If governance logic relies purely on raw code, safety boundaries drift. Managing boundaries via formal policies as code (PaC) allows versioned guarantees.

## Bundle Lifecycle
Draft -> Proposed -> Under Review -> Review Approved -> Promotion Ready -> Active -> Deprecated -> Archived

## Precedence and Overlays
- Precedence order explicitly defines conflict resolution logic.
- Overlays mutate effective policies dynamically, allowing safe temporary exceptions (like emergency interventions) without redefining base rules.

## Change Requests and Reviews
Every policy mutation runs through a change request pipeline that diffs the modifications and calculates safety risks based on scopes.

## Integration
- **Control Planes, Cohorts, Approvals, Evidence**: All these subsystems evaluate operations against loaded policy bundles rather than using static constants.

## Future Path
Signed bundles, remote registries, formal proofs, and distributed policy application.
