INSERT INTO processes (process_id, process_name) VALUES
  ('P-CVD', 'PECVD Oxide'),
  ('P-ETCH', 'Spacer Etch')
ON CONFLICT (process_id) DO NOTHING;

INSERT INTO recipes (recipe_id, process_id, recipe_name, recipe_version) VALUES
  ('R-CVD-01', 'P-CVD', 'Oxide Deposition', 'v1.4'),
  ('R-ETCH-02', 'P-ETCH', 'Spacer Etch', 'v2.1')
ON CONFLICT (recipe_id) DO NOTHING;

INSERT INTO wafers (wafer_id, lot_id, recipe_id, status, slot_no, created_at) VALUES
  ('W-1001', 'L-2001', 'R-CVD-01', 'processed', 1, '2026-03-30T08:40:00Z'),
  ('W-1002', 'L-2001', 'R-CVD-01', 'processed', 2, '2026-03-30T08:55:00Z'),
  ('W-1003', 'L-2002', 'R-ETCH-02', 'hold', 3, '2026-03-30T09:30:00Z'),
  ('W-1004', 'L-2002', 'R-ETCH-02', 'queued', 4, '2026-03-30T09:45:00Z')
ON CONFLICT (wafer_id) DO UPDATE SET
  lot_id = EXCLUDED.lot_id,
  recipe_id = EXCLUDED.recipe_id,
  status = EXCLUDED.status,
  slot_no = EXCLUDED.slot_no,
  created_at = EXCLUDED.created_at;

INSERT INTO metrology_measurements (measurement_id, wafer_id, metric_name, metric_value, metric_unit, measured_at) VALUES
  ('M-1001', 'W-1001', 'sheet_res_ohm_sq', 40.6, 'ohm/sq', '2026-03-30T08:48:00Z'),
  ('M-1002', 'W-1002', 'sheet_res_ohm_sq', 42.8, 'ohm/sq', '2026-03-30T09:04:00Z'),
  ('M-1003', 'W-1003', 'thickness_nm', 111.4, 'nm', '2026-03-30T09:35:00Z'),
  ('M-1004', 'W-1004', 'thickness_nm', 109.9, 'nm', '2026-03-30T09:50:00Z')
ON CONFLICT (measurement_id) DO UPDATE SET
  wafer_id = EXCLUDED.wafer_id,
  metric_name = EXCLUDED.metric_name,
  metric_value = EXCLUDED.metric_value,
  metric_unit = EXCLUDED.metric_unit,
  measured_at = EXCLUDED.measured_at;
