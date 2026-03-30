import time
from fastapi import APIRouter
from app.schemas.common import QueryCypherRequest, QueryCypherResponse
from app.services.fab_data import (
    DOE_GROUP_CYPHER,
    FILTERED_WAFERS_CYPHER,
    LATEST_WAFERS_CYPHER,
    build_group_exploration,
    get_filtered_wafers,
    get_latest_wafers,
    rows_to_graph,
)

router = APIRouter(tags=["query_cypher"])


@router.post("/query/cypher", response_model=QueryCypherResponse)
async def query_cypher_endpoint(payload: QueryCypherRequest):
    t0 = time.perf_counter()
    normalized = payload.query.lower()
    params = payload.parameters or {}

    if "uc3" in normalized or "same period" in normalized or "doe" in normalized or params.get("mode") == "uc3":
        graph, rows, _source, _period = build_group_exploration(
            group_by=str(params.get("group_by", "lot_id")),
            same_period=bool(params.get("same_period", True)),
            limit=params.get("limit", 12),
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return QueryCypherResponse(
            result=graph,
            cypher=DOE_GROUP_CYPHER,
            row_count=len(rows),
            execution_time_ms=round(elapsed_ms, 2),
        )

    if "uc2" in normalized or "filtered wafers" in normalized or params.get("mode") == "uc2":
        rows, _source = get_filtered_wafers(
            limit=params.get("limit", 10),
            status=params.get("status"),
            recipe_id=params.get("recipe_id"),
            lot_id=params.get("lot_id"),
        )
        graph = rows_to_graph(rows)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return QueryCypherResponse(
            result=graph,
            cypher=FILTERED_WAFERS_CYPHER,
            row_count=len(graph.raw),
            execution_time_ms=round(elapsed_ms, 2),
        )

    if "latest wafers" in normalized or "match (w:wafer" in normalized:
        rows, _source = get_latest_wafers(limit=int(params.get("limit", 10)))
        graph = rows_to_graph(rows)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return QueryCypherResponse(
            result=graph,
            cypher=LATEST_WAFERS_CYPHER,
            row_count=len(graph.raw),
            execution_time_ms=round(elapsed_ms, 2),
        )

    rows, _source = get_latest_wafers(limit=10)
    graph = rows_to_graph(rows)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return QueryCypherResponse(
        result=graph,
        cypher=LATEST_WAFERS_CYPHER,
        row_count=len(graph.raw),
        execution_time_ms=round(elapsed_ms, 2),
    )
