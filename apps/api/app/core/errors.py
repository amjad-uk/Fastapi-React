from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.middleware.base import BaseHTTPMiddleware
import logging, uuid
logger = logging.getLogger(__name__)
class ServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message); self.message = message; self.status_code = status_code
async def service_error_handler(request: Request, exc: ServiceError):
    rid = request.headers.get("X-Request-ID", "-")
    logger.warning("service_error", extra={"request_id": rid, "detail": exc.message})
    return JSONResponse({"error": exc.message, "request_id": rid}, status_code=exc.status_code)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    rid = request.headers.get("X-Request-ID", "-")
    logger.info("validation_error", extra={"request_id": rid, "errors": exc.errors()})
    return JSONResponse({"error": "validation_error", "detail": exc.errors(), "request_id": rid}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)
async def unhandled_error_handler(request: Request, exc: Exception):
    rid = request.headers.get("X-Request-ID", "-")
    logger.exception("unhandled_error", extra={"request_id": rid})
    return JSONResponse({"error": "internal_server_error", "request_id": rid}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        response = await call_next(request); response.headers["X-Request-ID"] = rid; return response
