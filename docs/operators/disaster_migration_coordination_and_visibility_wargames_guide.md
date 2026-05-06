# Operator Guide: Disaster Migration Coordination & Visibility War-Games

## Disaster Migration Lanes
Migration requires explicit handoffs. Ensure that the source is fresh and not stale before proceeding.
Use `advance_migration_stage` and `verify_migration_checkpoint` to record progress.

## Coordination Drills
When handing off between teams (e.g., local operator to governance owner), you must preserve the freshness note and explicitly acknowledge the handoff.

## War-Games
During an operational war-game, the goal is not to fix the issue silently but to verify that visibility surfaces report the loss accurately. Suppressing signals is an explicit violation.
