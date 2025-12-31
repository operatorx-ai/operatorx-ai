from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/meta")
def meta() -> dict:
    return {"service": "operatorx-ai-backend", "version": "0.1.0"}
