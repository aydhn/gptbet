from typing import List, Dict, Any, Type
from .contracts import ScheduledJobDefinition, SchedulerRunContext, SchedulerManifest
from .strategies.base import BaseSchedulerStrategy
from .strategies.strict_sequential import StrictSequentialScheduler
from .strategies.dependency_batch import DependencyAwareBatchScheduler
from .strategies.conservative_ops import ConservativeOpsScheduler
from .strategies.summary_only import SummaryOnlyScheduler
from .strategies.recovery_runbook import RecoveryRunbookScheduler

class SchedulerRunner:
    def __init__(self, strategy_name: str = "strict_sequential"):
        self.strategy_map: Dict[str, Type[BaseSchedulerStrategy]] = {
            "strict_sequential": StrictSequentialScheduler,
            "dependency_batch": DependencyAwareBatchScheduler,
            "conservative_ops": ConservativeOpsScheduler,
            "summary_only": SummaryOnlyScheduler,
            "recovery_runbook": RecoveryRunbookScheduler,
        }
        strategy_cls = self.strategy_map.get(strategy_name, StrictSequentialScheduler)
        self.strategy = strategy_cls()

    def run(self, jobs: List[ScheduledJobDefinition], context: SchedulerRunContext) -> SchedulerManifest:
        return self.strategy.execute(jobs, context)
