from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz", summary="Health check", description="Returns basic readiness information.")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "API is healthy"}

