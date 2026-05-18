import uuid
from typing import Callable, Awaitable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from pricelab_core.infrastructure.http.adapter.starlette_request import StarletteRequest
from pricelab_core.infrastructure.http.context.request_context import request_id_ctx
from pricelab_core.infrastructure.http.port.http_request import HttpRequest


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        adapted: HttpRequest = StarletteRequest(request)

        request_id = adapted.headers.get("X-Request-ID", str(uuid.uuid4().__str__()))
        request_id_ctx.set(request_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response