from fastapi import FastAPI

app = FastAPI(title="OperatorX AI Backend")


@app.get("/")
def root():
    return {"message": "OperatorX AI backend is running"}
from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI(title="OperatorX AI Backend")


@app.get("/")
def root():
    return {"message": "OperatorX AI backend is running"}


app.include_router(api_router, prefix="/api/v1")
