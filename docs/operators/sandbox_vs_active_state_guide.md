# Sandbox vs Active State Guide

## Isolation Guarantees
The simulation sandbox provides absolute isolation from the active production state:
- Active config files are not modified.
- Production databases and approval ledgers are untouched.
- Output manifests are routed to a distinct `data/sandbox` namespace.

## Leakage Prevention
All simulation components run transient overrides. Patches are applied to an isolated context and never persisted back to the main release channels automatically by this phase.
