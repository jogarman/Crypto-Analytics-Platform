from fastapi import FastAPI

from .api import (
    analytics_router,
    health_router,
    pairs_router,
)


def create_application() -> FastAPI:
    app = FastAPI(
        title="Crypto Analytics Platform API",
        version="0.1.0",
        description="Backend services for tracked pairs and analytics data.",
    )
    app.include_router(health_router)
    app.include_router(pairs_router)
    app.include_router(analytics_router)
    return app


app = create_application()

