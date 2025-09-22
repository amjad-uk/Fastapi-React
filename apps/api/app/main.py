from fastapi import FastAPI
from fastapi.middleware import Middleware
import logging, os
from .core.logging_config import configure_logging
from .core.errors import (service_error_handler, validation_error_handler, unhandled_error_handler, ServiceError, CorrelationIdMiddleware,)
from .core.middleware import cors_middleware
from .api.routers import users
from .core.config import settings
from fastapi.exceptions import RequestValidationError
from .core.observability import init_tracing, instrument_fastapi

configure_logging(settings.API_LOG_LEVEL)
logger = logging.getLogger(__name__)
init_tracing(service_name=settings.OTEL_SERVICE_NAME, endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)

middlewares = [Middleware(CorrelationIdMiddleware), Middleware(*cors_middleware)]
app = FastAPI(title="Users API", version="2.0.0", middleware=middlewares)
instrument_fastapi(app)

SENTRY_DSN = settings.SENTRY_DSN
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FastApiIntegration(), LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)], traces_sample_rate=float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "1.0")), environment=settings.ENVIRONMENT)

@app.get("/healthz")
async def healthz(): return {"status": "ok"}

app.include_router(users.router)

app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, unhandled_error_handler)
