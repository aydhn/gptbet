# Operators Guide: Federations, Proof Lanes, and Councils

This guide explains how to operate and monitor the continuity verification systems.

## Key Concepts
-   **Observatory Federations:** Groups of nodes providing observability. Monitor their status to ensure they aren't 'review_only' or 'caveated'.
-   **Scheduler Proof Lanes:** Conduits for proof packets. Ensure packets are fresh; stale packets degrade the lane.
-   **Audit Pulse Councils:** Forums for resolving edge cases. A council needs sufficient evidence quorum to reach a 'verified' decision.

## Common Operations
-   `run-hardening-pack-17`: Runs the full verification suite.
-   `preview-*`: Use preview commands to inspect specific components (e.g., `preview-observatory-federation-report`).
