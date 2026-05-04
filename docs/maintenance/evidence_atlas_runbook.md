# Evidence Atlas Maintenance Runbook

## Handling Stale Atlases
1. Run `preview-evidence-atlases` to identify stale nodes.
2. Trace the lineage to the source (e.g., a stale dashboard snapshot).
3. Refresh the source system to clear the staleness block.

## Handling Mesh Pressure
1. Run `preview-assurance-meshes` to identify degraded paths.
2. Investigate the source of pressure (e.g., alert density, stale packet density).
3. Address the underlying issues to relieve backpressure.

## Handling Blocked Clearing Councils
1. Run `preview-clearing-councils` to identify open cases.
2. Provide missing evidence or achieve quorum to resolve the conflict.
