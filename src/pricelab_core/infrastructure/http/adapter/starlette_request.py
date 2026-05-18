from starlette.requests import Request

class StarletteRequest:
    def __init__(self, request: Request):
        self._request = request

    @property
    def headers(self) -> dict[str, str]:
        return dict(self._request.headers)
