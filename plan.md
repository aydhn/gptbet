1. **Define Pydantic Contracts**: Implement `sports_signal_bot/scheduler/contracts.py` containing data structures such as `ScheduledJobDefinition`, `SlotScheduleRecord`, `JobStateTransitionRecord`, `SchedulerManifest`, etc.
2. **Implement Core Scheduler Modules**: Create modules `slots.py`, `jobs.py`, `dependencies.py`, `preconditions.py`, `postconditions.py`, `retries.py`, `catchup.py`, `idempotency.py`, `runbooks.py`, `adapters.py`, `manifests.py`.
3. **Implement Execution Engine and Strategies**: Create `runner.py` and `strategies/*.py` (Base, StrictSequential, DependencyBatch, ConservativeOps, SummaryOnly, RecoveryRunbook) to handle the execution state machine.
4. **Build Tests**: Create all necessary tests under `tests/scheduler/` (e.g., `test_dependency_graph.py`, `test_scheduler_runner.py`, etc.).
5. **Add Config Examples**: Create YAML config examples in `configs/scheduler/`.
6. **Integrate with CLI**: Add commands `run-scheduler`, `preview-slot-plan`, etc. to `sports_signal_bot/main.py` or equivalent.
7. **Documentation**: Update `README.md` and add `docs/scheduled_orchestration_architecture.md`.
8. **Pre-commit**: Complete pre-commit instructions.
9. **Submit**: Finalize and submit the changes.
