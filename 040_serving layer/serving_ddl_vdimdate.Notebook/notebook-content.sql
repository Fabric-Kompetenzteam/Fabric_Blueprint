-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "sqldatawarehouse"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "555cd4d6-87bd-49c3-b473-7e83cb83f1eb",
-- META       "default_lakehouse_name": "Blueprint_LH",
-- META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "555cd4d6-87bd-49c3-b473-7e83cb83f1eb"
-- META         }
-- META       ]
-- META     },
-- META     "warehouse": {
-- META       "default_warehouse": "1859e201-543e-44fb-9243-bf794bc3b5b4",
-- META       "known_warehouses": [
-- META         {
-- META           "id": "1859e201-543e-44fb-9243-bf794bc3b5b4",
-- META           "type": "Lakewarehouse"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- CELL ********************

CREATE VIEW serving.V_Dim_Date AS
SELECT
    DateID,
    FullDate,
    Day,
    Month,
    Year
FROM curated.dim_date;

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
