import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from pricelab_core.infrastructure.http.context.request_context import request_id_ctx


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        default_request_id: str = uuid.uuid4().__str__()
        request_id = request.headers.get("X-Request-ID", default_request_id)

        request_id_ctx.set(request_id)

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id
        return response