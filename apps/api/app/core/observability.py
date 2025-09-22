import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

def _normalize_http_endpoint(ep: str) -> str:
    if not ep:
        return ep
    if ep.endswith("/v1/traces"):
        return ep
    return ep.rstrip("/") + "/v1/traces"

def init_tracing(service_name: str, endpoint: str | None):
    if not endpoint: return
    endpoint = _normalize_http_endpoint(endpoint)
    resource = Resource.create({"service.name": service_name, "service.version": "1.0.0", "deployment.environment": os.getenv("ENVIRONMENT", "local")})
    provider = TracerProvider(resource=resource); trace.set_tracer_provider(provider)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    LoggingInstrumentor().instrument(set_logging_format=True)

def instrument_fastapi(app): FastAPIInstrumentor.instrument_app(app)
