-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "555cd4d6-87bd-49c3-b473-7e83cb83f1eb",
-- META       "default_lakehouse_name": "Blueprint_LH",
-- META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "b52127d0-485c-4fb0-b7ee-b8d80858f144"
-- META         },
-- META         {
-- META           "id": "555cd4d6-87bd-49c3-b473-7e83cb83f1eb"
-- META         }
-- META       ]
-- META     },
-- META     "environment": {}
-- META   }
-- META }

-- MARKDOWN ********************

-- #### Erstellung der Dim Product Tabelle

-- CELL ********************

CREATE TABLE IF NOT EXISTS curated.dim_product (
    ItemID BIGINT,
    ItemName STRING,
    ItemInfo STRING
);

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
