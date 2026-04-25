from typing import Any, Dict, Optional

from .base import BaseBenchmark
from .bookmaker_implied import BookmakerImpliedBenchmark
from .majority_benchmark import MajorityClassBenchmark
from .random_benchmark import RandomBenchmark
from .rating_placeholder import SimpleRatingBenchmark
from .uniform_benchmark import UniformProbBenchmark


class BenchmarkFactory:
    def __init__(self):
        self._benchmarks: Dict[str, BaseBenchmark] = {
            "random": RandomBenchmark(),
            "uniform": UniformProbBenchmark(),
            "majority": MajorityClassBenchmark(),
            "bookmaker_implied": BookmakerImpliedBenchmark(),
            "rating": SimpleRatingBenchmark(),
        }

    def get_benchmark(self, name: str) -> Optional[BaseBenchmark]:
        return self._benchmarks.get(name)

    def register(self, name: str, benchmark: BaseBenchmark):
        self._benchmarks[name] = benchmark


BENCHMARK_FACTORY = BenchmarkFactory()
