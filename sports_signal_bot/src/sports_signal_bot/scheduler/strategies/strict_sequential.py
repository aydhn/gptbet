from typing import List, Dict, Any
from .base import BaseSchedulerStrategy
from ..contracts import ScheduledJobDefinition, SchedulerRunContext, SchedulerManifest, JobState, ScheduledExecutionRecord, SchedulerSummaryRecord
from ..dependencies import DependencyGraph
import datetime

class StrictSequentialScheduler(BaseSchedulerStrategy):
    def plan(self, jobs: List[ScheduledJobDefinition], context: SchedulerRunContext) -> List[str]:
        graph = DependencyGraph(jobs)
        return graph.topologically_order_jobs()

    def execute(self, jobs: List[ScheduledJobDefinition], context: SchedulerRunContext) -> SchedulerManifest:
        graph = DependencyGraph(jobs)
        order = graph.topologically_order_jobs()

        job_map = {j.job_name: j for j in jobs}
        execution_states = {}
        executions = []

        summary = SchedulerSummaryRecord(planned_jobs=len(jobs))

        for job_name in order:
            job = job_map[job_name]

            # Simple simulation of execution
            if context.mode == "dry_run":
                state = JobState.dry_run_only
            else:
                if graph.resolve_dependency_readiness(job_name, execution_states):
                    state = JobState.succeeded
                    summary.executed_jobs += 1
                else:
                    state = JobState.blocked_by_dependency
                    summary.blocked_by_dependency_counts += 1

            execution_states[job_name] = state
            executions.append(ScheduledExecutionRecord(
                schedule_run_id=context.schedule_run_id,
                job_name=job_name,
                slot_id=context.slot.slot_id,
                date=context.slot.date,
                planned_time=datetime.datetime.utcnow(),
                state_after=state
            ))

        return SchedulerManifest(
            schedule_run_id=context.schedule_run_id,
            slot_id=context.slot.slot_id,
            mode=context.mode,
            summary=summary,
            executions=executions
        )
