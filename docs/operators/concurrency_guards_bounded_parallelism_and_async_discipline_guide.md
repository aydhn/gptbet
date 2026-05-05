# Operator Guide: Concurrency Guards & Bounded Parallelism

## Overview
This guide covers how to operate the Concurrency Hardening Pack 03.

## Commands
* `python -m sports_signal_bot.main concurrency run-hardening-pack-03`: Runs the full suite of checks and outputs JSON manifests.
* `python -m sports_signal_bot.main concurrency preview-concurrency-guard-report`: Previews guard status.
* `python -m sports_signal_bot.main concurrency preview-parallelism-report`: Previews bounds on parallel execution plans.
* `python -m sports_signal_bot.main concurrency list-concurrency-hardening-strategies`: Lists available tuning strategies.

## Guardrails
- If a race condition is detected on a critical path, it is **release-blocking**.
- Unbounded parallelism is explicitly rejected by the `ConservativeConcurrencyHardeningStrategy`.
- Silent partial merges after a timeout are treated as a safety violation.
