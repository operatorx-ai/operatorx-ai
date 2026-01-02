import logging
from fastapi import FastAPI

# ------------------------------------------------------------
# API Route Groups
# ------------------------------------------------------------
# Core API routes (health, metadata, etc.)
from app.routes import router as api_router

# Agent orchestration and discovery routes
from app.agent_routes import router as agents_router

# Tier inspection and debugging routes
from app.tier_routes import router as tier_router

# Memory inspection/debug routes (Phase 2)
from app.memory_routes import router as memory_router

# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------
# Middleware responsible for injecting and propagating request_id
from app.middleware import RequestIdMiddleware


# ------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------
# Configure basic logging so CoreEngine, middleware, and route logs
# are visible during local development and testing.
# In later phases, this can be replaced with structured logging
# or external log aggregation (ELK, Azure Monitor, etc.).
logging.basicConfig(level=logging.INFO)


# ------------------------------------------------------------
# Application Initialization
# ------------------------------------------------------------
# Create the FastAPI application instance.
# This is the central entry point for the backend service.
app = FastAPI(title="OperatorX AI Backend")


# ------------------------------------------------------------
# Middleware Registration
# ------------------------------------------------------------
# Adds a unique X-Request-Id header to every request/response.
# The request_id is stored on request.state and propagated
# through the Core Engine, agents, and memory layer.
app.add_middleware(RequestIdMiddleware)


# ------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------
@app.get("/")
def root():
    """
    Root health endpoint.

    Intended for:
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

# Request-scoped memory inspection routes (Phase 2)
app.include_router(memory_router, prefix="/api/v1")
