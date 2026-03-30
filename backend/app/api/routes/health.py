from fastapi import APIRouter
from app.db import neo4j, postgres
from app.schemas.common import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_endpoint():
    return HealthResponse(
        status="ok",
        service="fabgraph-backend",
        version="0.1.0",
        neo4j_connected=neo4j.is_available(),
        postgres_connected=postgres.is_available(),
    )
