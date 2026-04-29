import time
from functools import wraps
from datetime import datetime, timezone
from typing import List, Dict, Optional
from .contracts import StepTimingRecord

class TimingRegistry:
    def __init__(self):
        self.records: List[StepTimingRecord] = []

    def add(self, record: StepTimingRecord):
        self.records.append(record)

    def get_all(self) -> List[StepTimingRecord]:
        return self.records

class PerformanceTimer:
    def __init__(self, name: str, registry: TimingRegistry):
        self.name = name
        self.registry = registry
        self.start_time = None
        self.start_dt = None

    def __enter__(self):
        self.start_dt = datetime.now(timezone.utc)
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (time.perf_counter() - self.start_time) * 1000
        self.registry.add(StepTimingRecord(
            step_name=self.name,
            duration_ms=duration,
            started_at=self.start_dt
        ))

def time_step(name: str, registry: TimingRegistry):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with PerformanceTimer(name, registry):
                return func(*args, **kwargs)
        return wrapper
    return decorator

class StepProfiler:
    def __init__(self, registry: TimingRegistry):
        self.registry = registry

    def summarize_component_timing(self) -> Dict[str, float]:
        summary = {}
        for r in self.registry.get_all():
            summary[r.step_name] = summary.get(r.step_name, 0.0) + r.duration_ms
        return summary

def detect_slow_steps(registry: TimingRegistry, threshold_ms: float) -> List[StepTimingRecord]:
    return [r for r in registry.get_all() if r.duration_ms > threshold_ms]
