from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.market import router as market_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(
    market_router,
    prefix="/market",
    tags=["market"]
    )

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    }
