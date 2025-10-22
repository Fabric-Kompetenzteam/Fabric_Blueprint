-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "ae307d1f-c19d-4a89-b373-3c58878cc08a",
-- META       "default_lakehouse_name": "Blueprint_LH",
-- META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "ae307d1f-c19d-4a89-b373-3c58878cc08a"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- MARKDOWN ********************

-- #### Erstellung der Dim Product Tabelle

-- CELL ********************

CREATE TABLE IF NOT EXISTS gold.dim_product (
    ItemID BIGINT,
    ItemName STRING,
    ItemInfo STRING,
    ValidFrom TIMESTAMP,
    ValidTo TIMESTAMP,
    IsCurrent BOOLEAN
);

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
