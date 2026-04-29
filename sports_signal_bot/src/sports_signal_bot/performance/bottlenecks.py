from typing import List
from .contracts import BottleneckRecord
from .profiling import TimingRegistry

class BottleneckReporter:
    def __init__(self, registry: TimingRegistry):
        self.registry = registry

    def build_bottleneck_report(self) -> List[BottleneckRecord]:
        records = []
        for r in self.registry.get_all():
            records.append(BottleneckRecord(
                component="System",
                step=r.step_name,
                duration_ms=r.duration_ms,
                impact_score=r.duration_ms / 1000.0
            ))
        records.sort(key=lambda x: x.duration_ms, reverse=True)
        return records
