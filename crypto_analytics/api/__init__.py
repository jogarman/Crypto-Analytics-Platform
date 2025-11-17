from .analytics import router as analytics_router
from .health import router as health_router
from .pairs import router as pairs_router

__all__ = [
    "analytics_router",
    "health_router",
    "pairs_router",
]

