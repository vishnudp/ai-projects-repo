from dataclasses import dataclass, field
from time import perf_counter
from typing import Dict


@dataclass
class RuntimeMetrics:
    counters: Dict[str, int] = field(default_factory=dict)
    timings_ms: Dict[str, float] = field(default_factory=dict)

    def increment(
        self,
        name: str,
        value: int = 1,
    ) -> None:
        self.counters[name] = (
            self.counters.get(name, 0) + value
        )

    def record_timing(
        self,
        name: str,
        started_at: float,
    ) -> float:
        elapsed_ms = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        self.timings_ms[name] = elapsed_ms

        return elapsed_ms

    def snapshot(self) -> dict:
        return {
            "counters": dict(self.counters),
            "timings_ms": dict(self.timings_ms),
        }


metrics = RuntimeMetrics()