from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.anomaly.presentation.api.controllers.anomaly_controller import (
    router as anomaly_router,
)
from src.core.infrastructure.database.session import engine
from src.inventory.presentation.api.controllers import (
    item_router,
    movement_router,
    warehouse_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events, such as database connection pooling.
    """
    # Yield control to the application
    yield

    # Clean up database engine on shutdown
    await engine.dispose()


app = FastAPI(
    title="Supply Chain Anomaly Management API",
    description="API for managing inventory movements and detecting anomalies.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS Middleware
# Allowing all origins for development, but should be restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API Versioning Router
api_v1_router = APIRouter(prefix="/api/v1")

# Include context routers
api_v1_router.include_router(anomaly_router)
api_v1_router.include_router(item_router)
api_v1_router.include_router(warehouse_router)
api_v1_router.include_router(movement_router)

# Include the versioned router in the main application
app.include_router(api_v1_router)


class HealthResponse(BaseModel):
    """Schema for health check response."""

    status: str
    version: str


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
)
async def health_check() -> HealthResponse:
    """Check if the API is running."""
    return HealthResponse(status="ok", version="1.0.0")
