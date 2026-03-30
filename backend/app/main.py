import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.query_sql import router as query_sql_router
from app.api.routes.query_cypher import router as query_cypher_router
from app.api.routes.schema import router as schema_router
from app.api.routes.health import router as health_router
from app.core.config import settings
import app.db.postgres as pg_db
import app.db.neo4j as neo4j_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_ok = pg_db.is_available()
    neo4j_ok = neo4j_db.is_available()
    logger.info(
        "FabGraph startup — PostgreSQL: %s | Neo4j: %s",
        "connected" if pg_ok else "unavailable (fallback mode)",
        "connected" if neo4j_ok else "unavailable (fallback mode)",
    )
    yield


app = FastAPI(title=settings.app_name, version=settings.version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(chat_router, prefix=settings.api_prefix)
app.include_router(query_sql_router, prefix=settings.api_prefix)
app.include_router(query_cypher_router, prefix=settings.api_prefix)
app.include_router(schema_router, prefix=settings.api_prefix)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "running",
    }
