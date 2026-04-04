from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationStatus:
    is_valid: bool
    reason: str | None = None
    exception: Exception | None = None

    def __bool__(self) -> bool:
        return self.is_valid

    @staticmethod
    def ok() -> ValidationStatus:
        return ValidationStatus(True)

    @staticmethod
    def fail(reason: str | None = None, exception: type[Exception] | Exception | None = None) -> ValidationStatus:
        if isinstance(exception, type):
            exception = exception(reason)
        return ValidationStatus(False, reason, exception)
