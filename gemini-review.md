Code Review
This pull request introduces OpenTelemetry distributed tracing to the Aura Platform, a significant and well-structured enhancement. The changes effectively instrument the API Gateway and Core Service, covering FastAPI, gRPC, SQLAlchemy, and LangChain, with Jaeger integration for trace visualization. My review focuses on improving code clarity, removing redundancy, and addressing potential breaking changes in the API. I've provided suggestions to correct a misleading example in the documentation and refactor duplicated telemetry setup code. Most importantly, I've highlighted two high-severity issues regarding breaking changes to the API response structures in the API Gateway, which should be addressed to ensure client compatibility.

api-gateway/src/main.py
Comment on lines 125 to +148
        result_type = response.WhichOneof("result")

        output = {
            "session_token": response.session_token,
            "status": result_type,
            "valid_until": response.valid_until_timestamp,
        }

        if result_type == "accepted":
            output["data"] = {
                "final_price": response.accepted.final_price,
                "reservation_code": response.accepted.reservation_code,
            }
            logger.info(
                "negotiation_accepted",
                final_price=response.accepted.final_price,
                reservation_code=response.accepted.reservation_code,
            )
        elif result_type == "countered":
            output["data"] = {
                "proposed_price": response.countered.proposed_price,
                "message": response.countered.human_message,
            }
            logger.info(
                "negotiation_countered",
                proposed_price=response.countered.proposed_price,
            )
        elif result_type == "ui_required":
            output["action_required"] = {
                "template": response.ui_required.template_id,
                "context": dict(response.ui_required.context_data),
            }
            logger.info(
                "negotiation_ui_required",
                template_id=response.ui_required.template_id,
            )
        elif result_type == "rejected":
            logger.info("negotiation_rejected")

        return output
        return MessageToDict(
            response, preserving_proto_field_name=False, use_integers_for_enums=False
        )
@gemini-code-assist
gemini-code-assist bot
24 minutes ago
high

The refactoring to use MessageToDict introduces a breaking change in the API response for the /v1/negotiate endpoint. The JSON structure is now different from the previous implementation. For example, the status and data fields are gone, replaced by a structure mirroring the protobuf message (e.g., {"accepted": ...}). If this is unintentional, you should revert to manual dictionary creation or transform the output of MessageToDict to match the old structure to maintain API compatibility.

@zaebee	Reply...
api-gateway/src/main.py
Comment on lines +190 to +193
        logger.info("search_completed", result_count=len(response.results))
        return MessageToDict(
            response, preserving_proto_field_name=False, use_integers_for_enums=False
        )
@gemini-code-assist
gemini-code-assist bot
24 minutes ago
high

Similar to the /v1/negotiate endpoint, using MessageToDict here introduces a breaking change in the response structure for /v1/search. The field names in the results array are changed from custom names (like id, price, score, details) to camelCase names from the protobuf definition (itemId, basePrice, similarityScore, descriptionSnippet). Additionally, the similarity_score is no longer rounded. If this is not intended, you should stick to manual serialization to maintain API compatibility.

@zaebee	Reply...
TELEMETRY.md
Comment on lines +132 to +133
  "trace_id": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
  "span_id": "ab1c2d3e4f5g6h7i",
@gemini-code-assist
gemini-code-assist bot
24 minutes ago
medium

The example trace_id and span_id in the log output contain non-hexadecimal characters (e.g., 'g', 'h', 'p'). Trace and span IDs are represented as hexadecimal strings. This example could be misleading for developers trying to understand the log format. Please update them to use valid hex characters (0-9, a-f).

Suggested change
  "trace_id": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
  "span_id": "ab1c2d3e4f5g6h7i",
  "trace_id": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d",
  "span_id": "ab1c2d3e4f5a6b7c",
@zaebee	Reply...
api-gateway/src/telemetry.py
Comment on lines +19 to +20
    # Use provided OTLP endpoint or default to Jaeger
    otlp_endpoint = otlp_endpoint or "http://jaeger:4317"
@gemini-code-assist
gemini-code-assist bot
24 minutes ago
medium

This logic is redundant because the otlp_endpoint parameter already has a default value in the function signature. If an empty string is passed from the configuration, it will be overridden here, which might be confusing. It's better to rely on the default value defined in the function signature for consistency and remove these lines.

@zaebee	Reply...
core-service/src/telemetry.py
Comment on lines +1 to +41
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def init_telemetry(service_name: str, otlp_endpoint: str = "http://jaeger:4317") -> trace.Tracer:
    """
    Initialize OpenTelemetry tracing with OTLP exporter.
    Args:
        service_name: Name of the service for resource attribution
        otlp_endpoint: OTLP endpoint for exporting traces
    Returns:
        Configured tracer instance
    """
    # Use provided OTLP endpoint or default to Jaeger
    otlp_endpoint = otlp_endpoint or "http://jaeger:4317"

    # Create resource with service name
    resource = Resource.create({"service.name": service_name})

    # Set up tracer provider with resource
    provider = TracerProvider(resource=resource)

    # Set up OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)

    # Add batch span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)

    # Set as global tracer provider
    trace.set_tracer_provider(provider)

    # Get tracer for the service
    tracer = trace.get_tracer(service_name)

    return tracer
@gemini-code-assist
gemini-code-assist bot
24 minutes ago
medium

This file is identical to api-gateway/src/telemetry.py. To avoid code duplication and improve maintainability, consider creating a shared library or package for common utilities like telemetry initialization that can be used by both core-service and api-gateway.

@zaebee	Reply...
core-service/src/telemetry.py
Comment on lines +19 to +20
    # Use provided OTLP endpoint or default to Jaeger
    otlp_endpoint = otlp_endpoint or "http://jaeger:4317"
@gemini-code-assist
gemini-code-assist bot
24 minutes ago
medium

This logic is redundant because the otlp_endpoint parameter already has a default value in the function signature. If an empty string is passed from the configuration, it will be overridden here, which might be confusing. It's better to rely on the default value defined in the function signature for consistency and remove these lines.
