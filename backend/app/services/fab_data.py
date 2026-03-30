from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from app.core.config import settings
from app.db import neo4j, postgres
from app.schemas.common import GraphEdge, GraphNode, GraphResult


LATEST_WAFERS_QUERY = "-- uc1 latest wafers\nSELECT * FROM latest_wafers LIMIT 10;"
LATEST_WAFERS_CYPHER = "// uc1 latest wafers\nMATCH (w:Wafer)-[:BELONGS_TO]->(l:Lot)-[:USES_RECIPE]->(r:Recipe) RETURN w, l, r ORDER BY w.created_at DESC LIMIT 10"
FILTERED_WAFERS_QUERY = "-- uc2 filtered wafers\nSELECT * FROM latest_wafers WHERE status = :status;"
FILTERED_WAFERS_CYPHER = "// uc2 filtered wafers\nMATCH (w:Wafer)-[:BELONGS_TO]->(l:Lot)-[:USES_RECIPE]->(r:Recipe) RETURN w, l, r // filtered wafer slice"
DOE_GROUP_CYPHER = "// uc3 same period / DOE exploration\nMATCH (w:Wafer)-[:BELONGS_TO]->(l:Lot)-[:USES_RECIPE]->(r:Recipe) RETURN w, l, r // grouped exploration"


ALLOWED_STATUSES = {"queued", "hold", "processed"}


def _read_sample_rows() -> list[dict[str, Any]]:
    sample_path = Path(settings.sample_data_path)
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    return list(payload["latest_wafers"])


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def _normalize_status(status: Any) -> str | None:
    if status is None:
        return None
    normalized = str(status).strip().lower()
    return normalized if normalized in ALLOWED_STATUSES else None


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_limit(limit: Any, default: int = 10, minimum: int = 1, maximum: int = 50) -> int:
    try:
        value = int(limit)
    except Exception:
        return default
    return max(minimum, min(maximum, value))


def _apply_filters(rows: list[dict[str, Any]], *, status: str | None = None, recipe_id: str | None = None, lot_id: str | None = None) -> list[dict[str, Any]]:
    filtered = rows
    if status:
        filtered = [row for row in filtered if str(row.get("status", "")).lower() == status]
    if recipe_id:
        filtered = [row for row in filtered if row.get("recipe_id") == recipe_id]
    if lot_id:
        filtered = [row for row in filtered if row.get("lot_id") == lot_id]
    return filtered


def get_latest_wafers(limit: int = 10) -> tuple[list[dict[str, Any]], str]:
    limit = _coerce_limit(limit)
    try:
        rows = postgres.fetch_latest_wafers(limit=limit)
        if rows:
            return rows, "postgres"
    except Exception:
        pass
    return _read_sample_rows()[:limit], "sample"


def get_filtered_wafers(
    *,
    limit: int = 10,
    status: str | None = None,
    recipe_id: str | None = None,
    lot_id: str | None = None,
) -> tuple[list[dict[str, Any]], str]:
    limit = _coerce_limit(limit)
    status = _normalize_status(status)
    recipe_id = _normalize_text(recipe_id)
    lot_id = _normalize_text(lot_id)

    rows, source = get_latest_wafers(limit=50)
    filtered = _apply_filters(rows, status=status, recipe_id=recipe_id, lot_id=lot_id)
    return filtered[:limit], source


def build_basic_stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metric_values = [value for row in rows if (value := _safe_float(row.get("metric_value"))) is not None]
    statuses = Counter(str(row.get("status", "unknown")).lower() for row in rows)
    recipe_counts = Counter(str(row.get("recipe_id", "unknown")) for row in rows)
    lots = sorted({str(row.get("lot_id")) for row in rows if row.get("lot_id") is not None})

    stats: dict[str, Any] = {
        "row_count": len(rows),
        "status_counts": dict(statuses),
        "recipe_counts": dict(recipe_counts),
        "lot_ids": lots,
    }
    if metric_values:
        stats["metric_value"] = {
            "count": len(metric_values),
            "min": round(min(metric_values), 3),
            "max": round(max(metric_values), 3),
            "avg": round(mean(metric_values), 3),
        }
    return stats


def build_chart_config(rows: list[dict[str, Any]], *, preferred_x: str = "wafer_id") -> dict[str, Any]:
    x_key = preferred_x if rows and preferred_x in rows[0] else ("lot_id" if rows and "lot_id" in rows[0] else "_index")
    return {
        "chartType": "bar",
        "xKey": x_key,
        "title": "metric_value overview",
    }


def rows_to_graph(rows: list[dict[str, Any]]) -> GraphResult:
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    seen_nodes: set[str] = set()
    seen_edges: set[str] = set()

    for row in rows:
        wafer_node_id = f"wafer-{row['wafer_id']}"
        lot_node_id = f"lot-{row['lot_id']}"
        recipe_node_id = f"recipe-{row['recipe_id']}"

        wafer_props = {
            "wafer_id": row["wafer_id"],
            "lot_id": row["lot_id"],
            "recipe_id": row["recipe_id"],
            "status": row["status"],
            "slot_no": row.get("slot_no"),
            "created_at": row.get("created_at"),
            "metric_name": row.get("metric_name"),
            "metric_value": row.get("metric_value"),
            "metric_unit": row.get("metric_unit"),
        }
        lot_props = {
            "lot_id": row["lot_id"],
            "process_name": row.get("process_name"),
        }
        recipe_props = {
            "recipe_id": row["recipe_id"],
            "recipe_name": row.get("recipe_name"),
            "recipe_version": row.get("recipe_version"),
        }

        if wafer_node_id not in seen_nodes:
            nodes.append(GraphNode(id=wafer_node_id, labels=["Wafer"], properties=wafer_props))
            seen_nodes.add(wafer_node_id)
        if lot_node_id not in seen_nodes:
            nodes.append(GraphNode(id=lot_node_id, labels=["Lot"], properties=lot_props))
            seen_nodes.add(lot_node_id)
        if recipe_node_id not in seen_nodes:
            nodes.append(GraphNode(id=recipe_node_id, labels=["Recipe"], properties=recipe_props))
            seen_nodes.add(recipe_node_id)

        edge_id = f"{wafer_node_id}-belongs-{lot_node_id}"
        if edge_id not in seen_edges:
            edges.append(GraphEdge(id=edge_id, type="BELONGS_TO", source=wafer_node_id, target=lot_node_id, properties={"slot_no": row.get("slot_no")}))
            seen_edges.add(edge_id)

        recipe_edge_id = f"{lot_node_id}-uses-{recipe_node_id}"
        if recipe_edge_id not in seen_edges:
            edges.append(GraphEdge(id=recipe_edge_id, type="USES_RECIPE", source=lot_node_id, target=recipe_node_id, properties={}))
            seen_edges.add(recipe_edge_id)

    return GraphResult(nodes=nodes, edges=edges, raw=rows)


def latest_wafers_summary(rows: list[dict[str, Any]], source: str) -> str:
    if not rows:
        return f"No wafer rows available ({source})."
    wafer_ids = ", ".join(row["wafer_id"] for row in rows[:3])
    suffix = "" if len(rows) <= 3 else f" 외 {len(rows) - 3}개"
    return f"Latest wafers from {source}: {wafer_ids}{suffix}"


def filtered_wafers_summary(rows: list[dict[str, Any]], source: str, *, status: str | None = None, recipe_id: str | None = None, lot_id: str | None = None) -> str:
    filters = [
        f"status={status}" if status else None,
        f"recipe_id={recipe_id}" if recipe_id else None,
        f"lot_id={lot_id}" if lot_id else None,
    ]
    filter_text = ", ".join(part for part in filters if part) or "no explicit filter"
    stats = build_basic_stats(rows)
    metric = stats.get("metric_value")
    metric_text = ""
    if metric:
        metric_text = f", metric avg={metric['avg']} min={metric['min']} max={metric['max']}"
    return f"Filtered wafers from {source}: {stats['row_count']} rows ({filter_text}){metric_text}"


def build_group_exploration(
    *,
    group_by: str = "lot_id",
    same_period: bool = True,
    limit: int = 12,
) -> tuple[GraphResult, list[dict[str, Any]], str, str]:
    limit = _coerce_limit(limit, default=12, maximum=50)
    rows, fallback_source = get_latest_wafers(limit=50)
    raw_rows = rows[:]

    if neo4j.is_available():
        source = "neo4j+postgres"
    else:
        source = f"fallback:{fallback_source}"

    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in raw_rows:
        key = str(row.get(group_by) or "unknown")
        buckets[key].append(row)

    if same_period:
        period_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in raw_rows:
            created_at = str(row.get("created_at") or "")
            period_key = created_at[:10] if len(created_at) >= 10 else "unknown-date"
            period_buckets[period_key].append(row)
        if period_buckets:
            period_key, period_rows = sorted(period_buckets.items(), key=lambda item: (-len(item[1]), item[0]))[0]
            buckets = defaultdict(list)
            for row in period_rows:
                key = str(row.get(group_by) or "unknown")
                buckets[key].append(row)
            period_source = period_key
        else:
            period_source = "unknown-date"
    else:
        period_source = "all-period"

    group_rows: list[dict[str, Any]] = []
    for group_key, group_items in sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0]))[:limit]:
        metric_values = [value for row in group_items if (value := _safe_float(row.get("metric_value"))) is not None]
        status_counts = Counter(str(row.get("status", "unknown")).lower() for row in group_items)
        representative = group_items[0]
        group_rows.append(
            {
                "group_by": group_by,
                "group_key": group_key,
                "period": period_source,
                "wafer_count": len(group_items),
                "metric_avg": round(mean(metric_values), 3) if metric_values else None,
                "metric_min": round(min(metric_values), 3) if metric_values else None,
                "metric_max": round(max(metric_values), 3) if metric_values else None,
                "dominant_status": status_counts.most_common(1)[0][0] if status_counts else None,
                "recipe_id": representative.get("recipe_id"),
                "lot_id": representative.get("lot_id"),
                "source": source,
            }
        )

    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    root_id = f"exploration-{group_by}-{period_source}"
    nodes.append(
        GraphNode(
            id=root_id,
            labels=["Exploration"],
            properties={"group_by": group_by, "period": period_source, "source": source},
        )
    )

    for row in group_rows:
        group_node_id = f"group-{group_by}-{row['group_key']}"
        nodes.append(
            GraphNode(
                id=group_node_id,
                labels=["Group"],
                properties={
                    "group_key": row["group_key"],
                    "group_by": group_by,
                    "wafer_count": row["wafer_count"],
                    "metric_avg": row["metric_avg"],
                    "dominant_status": row["dominant_status"],
                },
            )
        )
        edges.append(
            GraphEdge(
                id=f"{root_id}-{group_node_id}",
                type="HAS_GROUP",
                source=root_id,
                target=group_node_id,
                properties={"period": period_source},
            )
        )
        recipe_id = row.get("recipe_id")
        if recipe_id:
            recipe_node_id = f"recipe-{recipe_id}"
            if not any(node.id == recipe_node_id for node in nodes):
                nodes.append(GraphNode(id=recipe_node_id, labels=["Recipe"], properties={"recipe_id": recipe_id}))
            edges.append(
                GraphEdge(
                    id=f"{group_node_id}-{recipe_node_id}",
                    type="USES_RECIPE",
                    source=group_node_id,
                    target=recipe_node_id,
                    properties={},
                )
            )

    return GraphResult(nodes=nodes, edges=edges, raw=group_rows), group_rows, source, period_source


def group_exploration_summary(rows: list[dict[str, Any]], source: str, *, group_by: str, period: str) -> str:
    if not rows:
        return f"No grouped rows available ({source})."
    leaders = ", ".join(f"{row['group_key']}({row['wafer_count']})" for row in rows[:3])
    suffix = "" if len(rows) <= 3 else f" 외 {len(rows) - 3}개 그룹"
    return f"Group exploration from {source}: {group_by} 기준 {period}, {leaders}{suffix}"
