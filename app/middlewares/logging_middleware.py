from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
from starlette.requests import Request
from starlette.responses import Response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid4())
        request.state.ip = request.client.host
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response
