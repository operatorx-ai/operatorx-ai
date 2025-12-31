from fastapi import FastAPI
from app.routes import router as api_router
from app.agent_routes import router as agents_router

app = FastAPI(title="OperatorX AI Backend")


@app.get("/")
def root():
    return {"message": "OperatorX AI backend is running"}


app.include_router(api_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")

