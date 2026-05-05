# Taxonomy of Concurrency Hardening

* **ConcurrencyGuardRecord**: Protects a specific surface (e.g., shared state, async join).
* **ParallelExecutionPlanRecord**: Bounds lane counts, worker pools, and queue budgets.
* **RaceProbeRunRecord**: Tracks a test run that perturbs execution scheduling.
* **SharedStateRecord**: Declares explicit ownership for mutable state.
* **IdempotencyRecord**: Associates a side-effect path with an idempotency key generator.
* **StaleReadRecord**: Tracks read access and verifies it falls within an acceptable drift window.
* **QueueDisciplineRecord**: Monitors queue length against a defined max capacity.
* **TimeoutRunRecord / CancellationRunRecord**: Evaluates behavior under simulated timeout or cancellation conditions.
