from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CircuitBreakerSettings:
    failure_threshold: int = 3
    recovery_timeout: float = 30.0
    success_threshold: int = 2
