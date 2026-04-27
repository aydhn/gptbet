from typing import Callable, Dict, List, Any
from sports_signal_bot.monitoring.contracts import HealthCheckRecord

class HealthCheckRegistry:
    _checks: Dict[str, List[Callable[..., List[HealthCheckRecord]]]] = {}
    @classmethod
    def register(cls, component: str) -> Callable:
        def decorator(func: Callable[..., List[HealthCheckRecord]]) -> Callable:
            if component not in cls._checks: cls._checks[component] = []
            cls._checks[component].append(func)
            return func
        return decorator
    @classmethod
    def get_checks(cls, component: str) -> List[Callable[..., List[HealthCheckRecord]]]:
        return cls._checks.get(component, [])
    @classmethod
    def get_all_components(cls) -> List[str]:
        return list(cls._checks.keys())
    @classmethod
    def clear(cls):
        cls._checks = {}
