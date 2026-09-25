from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.anomaly.presentation.api.controllers.anomaly_controller import (
    router as anomaly_router,
)
from src.core.domain.exceptions import (
    ConflictError,
    DomainError,
    EntityNotFoundError,
    EntityValidationError,
)
from src.core.infrastructure.database.session import engine
from src.core.presentation.api.schemas import RFC7807Error
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(
    request: Request,
    exc: EntityNotFoundError,
) -> JSONResponse:
    error_response = RFC7807Error(
        type="urn:api:error:not-found",
        title="Not Found",
        status=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response.model_dump(),
        media_type="application/problem+json",
    )


@app.exception_handler(ConflictError)
async def conflict_error_handler(
    request: Request,
    exc: ConflictError,
) -> JSONResponse:
    error_response = RFC7807Error(
        type="urn:api:error:conflict",
        title="Conflict",
        status=status.HTTP_409_CONFLICT,
        detail=str(exc),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response.model_dump(),
        media_type="application/problem+json",
    )


@app.exception_handler(EntityValidationError)
async def entity_validation_error_handler(
    request: Request,
    exc: EntityValidationError,
) -> JSONResponse:
    error_response = RFC7807Error(
        type="urn:api:error:validation",
        title="Unprocessable Entity",
        status=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail=str(exc),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_response.model_dump(),
        media_type="application/problem+json",
    )


@app.exception_handler(DomainError)
async def domain_error_handler(
    request: Request,
    exc: DomainError,
) -> JSONResponse:
    error_response = RFC7807Error(
        type="urn:api:error:domain-rule-violation",
        title="Bad Request",
        status=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.model_dump(),
        media_type="application/problem+json",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    type_map = {
        400: "urn:api:error:bad-request",
        401: "urn:api:error:unauthorized",
        403: "urn:api:error:forbidden",
        404: "urn:api:error:not-found",
        409: "urn:api:error:conflict",
        422: "urn:api:error:validation",
    }
    error_type = type_map.get(exc.status_code, "about:blank")
    error_response = RFC7807Error(
        type=error_type,
        title="HTTP Error",
        status=exc.status_code,
        detail=str(exc.detail),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
        media_type="application/problem+json",
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_response = RFC7807Error(
        type="urn:api:error:validation",
        title="Unprocessable Entity",
        status=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail=str(exc.errors()),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_response.model_dump(),
        media_type="application/problem+json",
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
