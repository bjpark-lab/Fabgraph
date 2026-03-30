CREATE TABLE IF NOT EXISTS processes (
  process_id TEXT PRIMARY KEY,
  process_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipes (
  recipe_id TEXT PRIMARY KEY,
  process_id TEXT NOT NULL REFERENCES processes(process_id),
  recipe_name TEXT NOT NULL,
  recipe_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wafers (
  wafer_id TEXT PRIMARY KEY,
  lot_id TEXT NOT NULL,
  recipe_id TEXT NOT NULL REFERENCES recipes(recipe_id),
  status TEXT NOT NULL,
  slot_no INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS metrology_measurements (
  measurement_id TEXT PRIMARY KEY,
  wafer_id TEXT NOT NULL REFERENCES wafers(wafer_id),
  metric_name TEXT NOT NULL,
  metric_value DOUBLE PRECISION NOT NULL,
  metric_unit TEXT NOT NULL,
  measured_at TIMESTAMPTZ NOT NULL
);

CREATE OR REPLACE VIEW wafer_latest_metrology AS
SELECT DISTINCT ON (wafer_id)
  wafer_id,
  metric_name,
  metric_value,
  metric_unit,
  measured_at
FROM metrology_measurements
ORDER BY wafer_id, measured_at DESC;
