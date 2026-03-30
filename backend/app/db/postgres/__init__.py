from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

from app.core.config import settings

try:
    import psycopg
    from psycopg.rows import dict_row
except Exception:  # pragma: no cover
    psycopg = None
    dict_row = None


LATEST_WAFERS_SQL = """
SELECT
    w.wafer_id,
    w.lot_id,
    w.recipe_id,
    w.status,
    w.slot_no,
    w.created_at,
    m.metric_name,
    m.metric_value,
    m.metric_unit,
    r.recipe_name,
    r.recipe_version,
    p.process_name
FROM wafers w
LEFT JOIN wafer_latest_metrology m ON m.wafer_id = w.wafer_id
LEFT JOIN recipes r ON r.recipe_id = w.recipe_id
LEFT JOIN processes p ON p.process_id = r.process_id
ORDER BY w.created_at DESC, w.wafer_id ASC
LIMIT %(limit)s
""".strip()


@contextmanager
def get_conn() -> Iterator[Any]:
    if psycopg is None:
        raise RuntimeError("psycopg is not installed")

    conn = psycopg.connect(
        settings.postgres_dsn,
        connect_timeout=settings.postgres_connect_timeout_s,
        row_factory=dict_row,
    )
    try:
        yield conn
    finally:
        conn.close()


def is_available() -> bool:
    if psycopg is None:
        return False
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True
    except Exception:
        return False


def fetch_latest_wafers(limit: int = 10) -> list[dict[str, Any]]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(LATEST_WAFERS_SQL, {"limit": limit})
            rows = cur.fetchall()
    return [dict(row) for row in rows]


def execute_raw_query(sql: str) -> list[dict[str, Any]]:
    """Execute arbitrary SQL for the dev query tool.

    Raises on DB unavailability or query error — callers should catch and fall back.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    return [dict(row) for row in rows]
