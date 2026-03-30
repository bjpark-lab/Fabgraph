from __future__ import annotations

from typing import Any

from app.core.config import settings

try:
    from neo4j import GraphDatabase
except Exception:  # pragma: no cover
    GraphDatabase = None


def get_driver() -> Any:
    if GraphDatabase is None:
        raise RuntimeError("neo4j driver is not installed")
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
        connection_timeout=settings.neo4j_connect_timeout_s,
    )


def is_available() -> bool:
    if GraphDatabase is None:
        return False
    try:
        driver = get_driver()
        try:
            driver.verify_connectivity()
        finally:
            driver.close()
        return True
    except Exception:
        return False
