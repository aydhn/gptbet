# Scheduled Orchestration Architecture

This document describes the orchestration architecture built for the sports signal bot, bringing together CLI commands, inference, dispatch, and monitoring into scheduled, dependency-aware pipelines.

## Why Scheduling?
Previously, components were run individually using the CLI. The scheduler coordinates these disparate tools automatically across pre-defined time windows (slots) by checking preconditions (e.g. system freezes or data staleness) and explicitly managing dependencies (e.g. inference must complete before dispatch).

## DAG-lite Design
The orchestration engine uses a lightweight, DAG-like dependency solver. Jobs specify their `dependency_names`, and the scheduler automatically performs a topological sort to sequence the execution order within a slot. Missing dependencies block execution and mark downstream jobs as `deferred`.

## Slot Model and Runbooks
A slot is a time window (e.g., morning, midday, evening, night_maintenance). Each slot allows certain job families to execute based on operator preferences.

Runbooks are predefined recipes (ordered job steps, normal paths, and degraded/freeze paths) that operators can inject into a schedule.

## Dependency and Precondition Engine
- **Preconditions**: Evaluate if it is safe to begin a job (e.g., check if system is frozen).
- **Dependencies**: Ensure the upstream jobs completed successfully (or with acceptable warnings) before execution.
- **Postconditions**: Validate that a completed job emitted the required artifacts (manifests).

## Retry / Catch-up / Idempotency
- **Retries**: Configurable policies allow immediate or backoff-based retries depending on the error classification.
- **Idempotency**: Execution ledgers record runs based on unique keys combining `date`, `slot_id`, and `job_name`. Duplicate executions are blocked.
- **Catch-up (Backfill)**: Policies determine if a job missed in a previous slot should be run or skipped (based on relevance window).

## State-Aware Scheduling
Schedulers alter their behavior dynamically:
- **Freeze Active**: Blocks sensitive jobs.
- **Degraded**: Some jobs fall back to safe modes (e.g., summary only).
- **Approval Pending**: Execution defers until manual approval is provided.

## Future Extensions
This phase lays the foundation. Future iterations can easily swap out the internal python runner with external tools like Airflow, Kubernetes cron jobs, or specialized task queues.
