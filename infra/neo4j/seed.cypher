MERGE (r1:Recipe {recipe_id: 'R-CVD-01'})
  SET r1.recipe_name = 'Oxide Deposition', r1.recipe_version = 'v1.4';
MERGE (r2:Recipe {recipe_id: 'R-ETCH-02'})
  SET r2.recipe_name = 'Spacer Etch', r2.recipe_version = 'v2.1';
MERGE (l1:Lot {lot_id: 'L-2001'})
MERGE (l2:Lot {lot_id: 'L-2002'})
MERGE (w1:Wafer {wafer_id: 'W-1001'}) SET w1.status = 'processed'
MERGE (w2:Wafer {wafer_id: 'W-1002'}) SET w2.status = 'processed'
MERGE (w3:Wafer {wafer_id: 'W-1003'}) SET w3.status = 'hold'
MERGE (w4:Wafer {wafer_id: 'W-1004'}) SET w4.status = 'queued'
MERGE (w1)-[:BELONGS_TO]->(l1)
MERGE (w2)-[:BELONGS_TO]->(l1)
MERGE (w3)-[:BELONGS_TO]->(l2)
MERGE (w4)-[:BELONGS_TO]->(l2)
MERGE (l1)-[:USES_RECIPE]->(r1)
MERGE (l2)-[:USES_RECIPE]->(r2);
