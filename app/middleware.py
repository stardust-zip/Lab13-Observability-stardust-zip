from __future__ import (
    annotations,  # Enables forward references in type hints (Python 3.7+)
)

import time  # For timing request processing duration
import uuid  # For generating unique 8-char hex IDs

from fastapi import Request  # FastAPI request object
from starlette.middleware.base import (
    BaseHTTPMiddleware,  # Base class for custom middleware
)
from structlog.contextvars import (  # Structlog context management
    bind_contextvars,
    clear_contextvars,
)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        clear_contextvars()  # Clear any leftover context from previous requests to prevent leakage

        incoming_id = request.headers.get(
            "x-request-id"
        )  # Check if client already sent a correlation ID
        if incoming_id:
            correlation_id = (
                incoming_id  # Use existing ID from client for distributed tracing
            )
        else:
            hex_part = uuid.uuid4().hex[:8]  # Generate random 8-character hex string
            correlation_id = f"req-{hex_part}"  # Format as "req-<8-char-hex>"

        bind_contextvars(
            correlation_id=correlation_id
        )  # Attach correlation ID to structlog context for all subsequent logs

        request.state.correlation_id = correlation_id  # Store correlation ID in request state for access in route handlers

        start = time.perf_counter()  # Record start time before processing request
        response = await call_next(request)  # Call the next middleware/handler in chain

        response_time = (
            time.perf_counter() - start
        ) * 1000  # Calculate processing time in milliseconds
        response.headers["x-request-id"] = (
            correlation_id  # Add correlation ID to response headers
        )
        response.headers["x-response-time-ms"] = str(
            response_time
        )  # Add processing time to response headers

        return response  # Return the response to the client

        # x-request-id: this DOES NOT depent on different value of message key in curl payload
        # x-response-time-ms: this DOES depent on value of message in curl payload (vary slightly -> longer prompt -> slightly more LLM latency)
