import asyncio
import json
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.common import ChatAction, ChatRequest, ChatResponse, StepInfo, ToolResult
from app.services.fab_data import (
    DOE_GROUP_CYPHER,
    FILTERED_WAFERS_CYPHER,
    LATEST_WAFERS_CYPHER,
    build_basic_stats,
    build_chart_config,
    build_group_exploration,
    filtered_wafers_summary,
    get_filtered_wafers,
    get_latest_wafers,
    group_exploration_summary,
    latest_wafers_summary,
    rows_to_graph,
)

router = APIRouter(tags=["chat"])


def _detect_intent(message: str) -> str:
    normalized = message.lower()
    if any(token in normalized for token in ["doe", "same period", "동일 기간", "same-period", "group", "그룹"]):
        return "uc3_group_exploration"
    if any(token in normalized for token in ["filter", "조건", "status", "통계", "평균", "hold", "queued", "processed"]):
        return "uc2_filtered_stats"
    return "uc1_latest_wafers"


def _extract_filters(message: str) -> dict[str, Any]:
    normalized = message.lower()
    filters: dict[str, Any] = {"limit": 10}
    for status in ["queued", "hold", "processed"]:
        if status in normalized:
            filters["status"] = status
            break
    for token in message.replace(",", " ").split():
        clean = token.strip()
        upper = clean.upper()
        if upper.startswith("R-"):
            filters["recipe_id"] = upper
        elif upper.startswith("L-"):
            filters["lot_id"] = upper
    return filters


def _uc1_payload() -> tuple[str, list[ChatAction], ToolResult, list[StepInfo]]:
    rows, source = get_latest_wafers(limit=10)
    graph = rows_to_graph(rows)
    summary = latest_wafers_summary(rows, source)
    message = (
        f"최신 wafer {len(rows)}개를 조회했습니다. 데이터 소스는 **{source}** 입니다.\n\n"
        + "\n".join(
            f"- **{row['wafer_id']}** · Lot {row['lot_id']} · {row['status']} · {row.get('metric_name')}={row.get('metric_value')} {row.get('metric_unit') or ''}"
            for row in rows
        )
    )
    return (
        message,
        [ChatAction(type="apply_query", query=LATEST_WAFERS_CYPHER), ChatAction(type="open_tab", tab="graph")],
        ToolResult(graph=graph, table=rows, cypher=LATEST_WAFERS_CYPHER, summary=summary),
        [
            StepInfo(tool="Router", tool_key="router", input="latest wafers", output=json.dumps({"intent": "uc1_latest_wafers"}, ensure_ascii=False)),
            StepInfo(tool="SqlAgent", tool_key="sql_agent", input="latest wafers", output=summary),
        ],
    )


def _uc2_payload(message_text: str) -> tuple[str, list[ChatAction], ToolResult, list[StepInfo]]:
    filters = _extract_filters(message_text)
    rows, source = get_filtered_wafers(**filters)
    graph = rows_to_graph(rows)
    stats = build_basic_stats(rows)
    summary = filtered_wafers_summary(rows, source, status=filters.get("status"), recipe_id=filters.get("recipe_id"), lot_id=filters.get("lot_id"))
    metric = stats.get("metric_value")
    metric_line = (
        f"- metric_value 평균 **{metric['avg']}**, 최소 **{metric['min']}**, 최대 **{metric['max']}**"
        if metric
        else "- metric_value 통계를 만들 수 있는 수치 데이터가 없습니다"
    )
    message = (
        f"조건 필터 wafer {len(rows)}개를 정리했습니다. 소스는 **{source}** 입니다.\n\n"
        f"- 상태 분포: {stats.get('status_counts', {})}\n"
        f"- 레시피 분포: {stats.get('recipe_counts', {})}\n"
        f"{metric_line}"
    )
    actions = [
        ChatAction(type="apply_query", query=FILTERED_WAFERS_CYPHER),
        ChatAction(type="open_tab", tab="table"),
        ChatAction(type="create_chart", chart_config=build_chart_config(rows)),
    ]
    tool_results = ToolResult(
        graph=graph,
        table=rows,
        chart={"rows": rows, **build_chart_config(rows)},
        cypher=FILTERED_WAFERS_CYPHER,
        summary=summary,
    )
    steps = [
        StepInfo(tool="Router", tool_key="router", input=message_text, output=json.dumps({"intent": "uc2_filtered_stats", "filters": filters}, ensure_ascii=False)),
        StepInfo(tool="SqlAgent", tool_key="sql_agent", input="filtered wafers", output=summary),
    ]
    return message, actions, tool_results, steps


def _uc3_payload(message_text: str) -> tuple[str, list[ChatAction], ToolResult, list[StepInfo]]:
    group_by = "recipe_id" if "recipe" in message_text.lower() else "lot_id"
    graph, rows, source, period = build_group_exploration(group_by=group_by, same_period=True)
    summary = group_exploration_summary(rows, source, group_by=group_by, period=period)
    leaders = "\n".join(
        f"- **{row['group_key']}** · wafer {row['wafer_count']}개 · avg={row['metric_avg']} · status={row['dominant_status']}"
        for row in rows[:5]
    )
    message = (
        f"동일 기간 그룹 탐색을 만들었습니다. 기준은 **{group_by}**, 기간은 **{period}**, 소스는 **{source}** 입니다.\n\n{leaders}"
    )
    actions = [
        ChatAction(type="apply_query", query=DOE_GROUP_CYPHER),
        ChatAction(type="open_tab", tab="graph"),
        ChatAction(type="create_chart", chart_config={"chartType": "bar", "xKey": "group_key"}),
    ]
    tool_results = ToolResult(
        graph=graph,
        table=rows,
        chart={"rows": rows, "chartType": "bar", "xKey": "group_key"},
        cypher=DOE_GROUP_CYPHER,
        summary=summary,
    )
    steps = [
        StepInfo(tool="Router", tool_key="router", input=message_text, output=json.dumps({"intent": "uc3_group_exploration", "group_by": group_by}, ensure_ascii=False)),
        StepInfo(tool="GraphAgent", tool_key="graph_agent", input="same period group exploration", output=summary),
    ]
    return message, actions, tool_results, steps


def _build_response(message_text: str) -> tuple[str, list[ChatAction], ToolResult, list[StepInfo]]:
    intent = _detect_intent(message_text)
    if intent == "uc3_group_exploration":
        return _uc3_payload(message_text)
    if intent == "uc2_filtered_stats":
        return _uc2_payload(message_text)
    return _uc1_payload()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    message, actions, tool_results, steps = _build_response(payload.message)
    return ChatResponse(message=message, actions=actions, tool_results=tool_results, steps=steps, reasoning=None)


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


async def _stream_router_plan(message: str):
    response_message, actions, tool_results, steps = _build_response(message)

    for step in steps:
        yield _sse({"type": "step_start", "tool": step.tool, "tool_key": step.tool_key, "input": step.input})
        await asyncio.sleep(0.05)
        yield _sse({"type": "step_end", "tool_key": step.tool_key, "output": step.output})
        await asyncio.sleep(0.05)

    for token in response_message.splitlines(keepends=True):
        yield _sse({"type": "token", "content": token})
        await asyncio.sleep(0.02)

    yield _sse({
        "type": "done",
        "actions": [action.model_dump() for action in actions],
        "tool_results": tool_results.model_dump(),
        "steps": [step.model_dump() for step in steps],
        "reasoning": None,
    })
    yield "data: [DONE]\n\n"


@router.post("/chat/stream")
async def chat_stream_endpoint(payload: ChatRequest):
    return StreamingResponse(
        _stream_router_plan(payload.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
