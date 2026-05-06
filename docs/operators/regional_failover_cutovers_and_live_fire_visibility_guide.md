# Operator Guide: Regional Hardening

## Overview
As an operator, you use the `regional-hardening` namespace to plan and rehearse failovers and staged cutovers. You do not just "flip a switch." Instead, you construct a rehearsal with expected lag and defined rollback readiness.

## Checkpoints
- Ensure that the primary has a freshness marker.
- Ensure that the target region has a readiness marker.
- Validate that the lag between them falls within configured boundaries.
- Track residue if a cutover is incomplete.
