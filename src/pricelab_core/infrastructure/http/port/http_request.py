from typing import Protocol


class HttpRequest(Protocol):

    @property
    def headers(self) -> dict[str, str]: ...