import logging
import os
import random
import time
from typing import Dict

import requests
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger

# ---- JSON logging to stdout ----
logger = logging.getLogger("sampleapp")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)

# ---- OpenTelemetry tracing ----
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

service_name = os.getenv("OTEL_SERVICE_NAME", "sampleapp")
resource = Resource.create({"service.name": service_name})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())  # respects OTEL_EXPORTER_OTLP_* envvars
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# ---- FastAPI app ----
app = FastAPI(title="Demo Observability App")
Instrumentator().instrument(app).expose(app)  # /metrics

FastAPIInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.get("/")
def read_root() -> Dict[str, str]:
    logger.info("root_called", extra={"route": "/", "status": "ok"})
    return {"status": "ok", "service": service_name}

@app.get("/work")
def do_work() -> Dict[str, str]:
    # Simulate a bit of work and an outgoing request (traced)
    with tracer.start_as_current_span("do_work"):
        time.sleep(random.uniform(0.05, 0.2))
        try:
            # a harmless outgoing call that will fail fast (to show spans/logs)
            requests.get("http://localhost:9", timeout=0.05)
        except Exception as e:
            logger.warning("work_external_call_failed", extra={"error": str(e)})
        return {"message": "did some work"}

@app.get("/error")
def error():
    logger.error("intentional_error", extra={"route": "/error"})
    raise RuntimeError("Bang!")
