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

-- #### Creating Dim Customer Table

-- CELL ********************

-- MAGIC %%sql
-- MAGIC CREATE SCHEMA IF NOT EXISTS gold

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- MARKDOWN ********************

-- ###### Schema Dim Customer

-- CELL ********************

-- MAGIC %%sql
-- MAGIC CREATE TABLE gold.dim_customer (
-- MAGIC     CustomerID INT,
-- MAGIC     CustomerName STRING,
-- MAGIC     Email STRING,
-- MAGIC     FirstName STRING,
-- MAGIC     LastName STRING
-- MAGIC )

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
