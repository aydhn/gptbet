from typing import List, Dict, Any
from abc import ABC, abstractmethod
from ..contracts import ScheduledJobDefinition, SchedulerRunContext, SchedulerManifest

class BaseSchedulerStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def plan(self, jobs: List[ScheduledJobDefinition], context: SchedulerRunContext) -> List[str]:
        pass

    @abstractmethod
    def execute(self, jobs: List[ScheduledJobDefinition], context: SchedulerRunContext) -> SchedulerManifest:
        pass
