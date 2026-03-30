import time
from fastapi import APIRouter
from app.schemas.common import QuerySqlRequest, QuerySqlResponse
from app.services.fab_data import (
    FILTERED_WAFERS_QUERY,
    LATEST_WAFERS_QUERY,
    build_basic_stats,
    get_filtered_wafers,
    get_latest_wafers,
)

router = APIRouter(tags=["query_sql"])


@router.post("/query/sql", response_model=QuerySqlResponse)
async def query_sql_endpoint(payload: QuerySqlRequest):
    t0 = time.perf_counter()
    normalized = payload.query.strip().lower()
    params = payload.parameters or {}

    if "uc2" in normalized or "filtered" in normalized or params.get("mode") == "uc2":
        rows, source = get_filtered_wafers(
            limit=params.get("limit", 10),
            status=params.get("status"),
            recipe_id=params.get("recipe_id"),
            lot_id=params.get("lot_id"),
        )
        stats = build_basic_stats(rows)
        stat_row = {"_section": "stats", **stats}
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return QuerySqlResponse(
            columns=list(rows[0].keys()) if rows else list(stat_row.keys()),
            rows=rows + [stat_row],
            row_count=len(rows),
            execution_time_ms=round(elapsed_ms, 2),
            source=source,
        )

    if "latest_wafers" in normalized or "from wafers" in normalized or normalized == "-- uc1 latest wafers":
        rows, source = get_latest_wafers(limit=int(params.get("limit", 10)))
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return QuerySqlResponse(
            columns=list(rows[0].keys()) if rows else [],
            rows=rows,
            row_count=len(rows),
            execution_time_ms=round(elapsed_ms, 2),
            source=source,
        )

    rows, source = get_latest_wafers(limit=10)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return QuerySqlResponse(
        columns=list(rows[0].keys()) if rows else [],
        rows=rows,
        row_count=len(rows),
        execution_time_ms=round(elapsed_ms, 2),
        source=source,
    )
