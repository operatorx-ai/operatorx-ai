import logging
from fastapi import FastAPI

# API route groups
from app.routes import router as api_router
from app.agent_routes import router as agents_router
from app.tier_routes import router as tier_router

# Middleware for request tracing
from app.middleware import RequestIdMiddleware


# ------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------
# Configure basic logging so engine and middleware logs
# are visible during local development and testing.
# In later phases, this can be replaced with structured
# logging or external log aggregation.
logging.basicConfig(level=logging.INFO)


# ------------------------------------------------------------
# Application Initialization
# ------------------------------------------------------------
# Create the FastAPI application instance.
# This serves as the central entry point for the backend.
app = FastAPI(title="OperatorX AI Backend")


# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------
# Adds a unique X-Request-Id header to every request/response.
# The request_id is stored on request.state and propagated
# through the Core Engine and agents for traceability.
app.add_middleware(RequestIdMiddleware)


# ------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------
@app.get("/")
def root():
    """
    Root health endpoint.

    Useful for:
    - Quick service checks
    - Load balancer health probes
    - Development verification
    """
    return {"message": "OperatorX AI backend is running"}


# ------------------------------------------------------------
# Versioned API Routes
# ------------------------------------------------------------
# All application APIs are mounted under /api/v1
# to support future versioning without breaking clients.

# Core utility and metadata routes
app.include_router(api_router, prefix="/api/v1")

# Agent orchestration and discovery routes
app.include_router(agents_router, prefix="/api/v1")

# Tier inspection and debugging routes
app.include_router(tier_router, prefix="/api/v1")
