---
owner: Principal Adoption Autopilot Engineer
family: operator_guides
freshness_window_days: 90
---

# Cohort Growth, Pause, and Rollback Guide

## Overview
This guide explains how to manage cohort lifecycles using the Phase 50 Cohort Autopilot.

## Managing Pauses
If a cohort is paused, check the `preview-cohort-pauses` CLI command. Common reasons include stale verification windows or temporary anomalies.

## Shrinking Scope
Shrinking allows you to retain adoption for healthy segments while removing problematic ones.

## Manual Overrides
Manual holds or stops always supersede autopilot decisions. Use these when you suspect an issue that the autopilot hasn't detected.
