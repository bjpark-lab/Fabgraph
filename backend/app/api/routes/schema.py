from fastapi import APIRouter
from app.schemas.common import SchemaResponse

router = APIRouter(tags=["schema"])

_PLACEHOLDER_SCHEMA = SchemaResponse(
    node_labels=["Wafer", "Lot", "Recipe", "Step", "Chamber", "Metrology", "Parameter"],
    relationship_types=["BELONGS_TO", "USES_RECIPE", "CONTAINS", "PROCESSED_IN", "MEASURED_BY"],
    node_properties={
        "Wafer":     ["wafer_id", "lot_id", "slot", "status", "created_at"],
        "Lot":       ["lot_id", "recipe_id", "equipment_id", "start_time"],
        "Recipe":    ["recipe_id", "name", "version", "process_type"],
        "Step":      ["step_id", "step_name", "sequence", "duration_s"],
        "Chamber":   ["chamber_id", "equipment_id", "type"],
        "Metrology": ["param_name", "value", "unit", "spec_min", "spec_max"],
        "Parameter": ["param_name", "value", "unit"],
    },
    relationship_properties={
        "BELONGS_TO":   ["slot"],
        "USES_RECIPE":  ["version"],
        "CONTAINS":     [],
        "PROCESSED_IN": ["start_time", "end_time"],
        "MEASURED_BY":  ["measurement_time"],
    },
)


@router.get("/schema", response_model=SchemaResponse)
async def schema_endpoint():
    # TODO: introspect real Neo4j schema via app.db.neo4j
    return _PLACEHOLDER_SCHEMA
