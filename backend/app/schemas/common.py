from pydantic import BaseModel, Field
from typing import Any


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "fabgraph-backend"
    version: str = "0.1.0"
    neo4j_connected: bool = False
    postgres_connected: bool = False


class PlaceholderPayload(BaseModel):
    query: str | None = None
    message: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class GraphNode(BaseModel):
    id: str
    labels: list[str]
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    type: str
    source: str
    target: str
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphResult(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
    raw: list[dict[str, Any]] = Field(default_factory=list)


class QueryCypherRequest(BaseModel):
    query: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class QueryCypherResponse(BaseModel):
    result: GraphResult
    cypher: str
    row_count: int
    execution_time_ms: float


class QuerySqlRequest(BaseModel):
    query: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class QuerySqlResponse(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    execution_time_ms: float
    source: str | None = None


class SchemaResponse(BaseModel):
    node_labels: list[str]
    relationship_types: list[str]
    node_properties: dict[str, list[str]]
    relationship_properties: dict[str, list[str]]


class ChatMessage(BaseModel):
    role: str
    content: str


class StepInfo(BaseModel):
    tool: str
    tool_key: str
    input: str
    output: str
    reasoning: str | None = None


class ToolResult(BaseModel):
    graph: GraphResult | None = None
    table: list[dict[str, Any]] | None = None
    chart: dict[str, Any] | None = None
    cypher: str | None = None
    summary: str | None = None


class ChatAction(BaseModel):
    type: str
    tab: str | None = None
    query: str | None = None
    node_id: str | None = None
    row_id: str | None = None
    filters: dict[str, Any] | None = None
    chart_config: dict[str, Any] | None = None
    series_id: str | None = None


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    message: str
    actions: list[ChatAction] = Field(default_factory=list)
    tool_results: ToolResult | None = None
    steps: list[StepInfo] = Field(default_factory=list)
    reasoning: str | None = None
