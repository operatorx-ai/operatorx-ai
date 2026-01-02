import logging
from fastapi import FastAPI

from app.routes import router as api_router
from app.agent_routes import router as agents_router
from app.tier_routes import router as tier_router
from app.middleware import RequestIdMiddleware

# Basic logging config so CoreEngine logs show up in the terminal
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="OperatorX AI Backend")

# Adds X-Request-Id to every request/response and stores request_id on request.state
app.add_middleware(RequestIdMiddleware)


@app.get("/")
def root():
    return {"message": "OperatorX AI backend is running"}


# Versioned API routes
app.include_router(api_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")
app.include_router(tier_router, prefix="/api/v1")
