from fastapi import APIRouter, Request

# Shared in-memory store used by the Core Engine
from app.core.memory import memory_store

# Router grouping all memory-related endpoints
router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("")
def get_memory(request: Request):
    """
    Retrieve request-scoped memory for the current request.

    How this endpoint is intended to be used:
    1. Call any API endpoint (e.g., /agents/orchestrate)
    2. That request generates a request_id via middleware
    3. Call /api/v1/memory using the SAME request context
    4. Inspect what the engine and agents stored during execution

    This endpoint is primarily for:
    - Debugging
    - Observability
    - Verifying context propagation (Phase 2)
    """

    # --------------------------------------------------------
    # Extract request_id from request.state
    # --------------------------------------------------------
    # The request_id is injected by RequestIdMiddleware.
    # If it does not exist, memory cannot be retrieved.
    request_id = getattr(request.state, "request_id", None)
    if not request_id:
        return {
            "ok": False,
            "error": "No request_id found on request"
        }

    # --------------------------------------------------------
    # Fetch memory record from the in-memory store
    # --------------------------------------------------------
    record = memory_store.get(request_id)
    if not record:
        return {
            "ok": False,
            "error": "No memory found for this request_id"
        }

    # --------------------------------------------------------
    # Return structured memory data
    # --------------------------------------------------------
    # This exposes only high-level diagnostic data.
    # Sensitive or internal-only data can be filtered later.
    return {
        "ok": True,
        "request_id": record.request_id,
        "tier": record.tier,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
        "data": record.data,
    }
