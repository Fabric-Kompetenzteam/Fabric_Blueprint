-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "303765a9-18c4-4cb6-aad4-c827f21b831d",
-- META       "default_lakehouse_name": "plansee_lh",
-- META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "303765a9-18c4-4cb6-aad4-c827f21b831d"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- MARKDOWN ********************

-- #### Erstellung der Dim Date Tabelle

-- CELL ********************

-- MAGIC %%sql 
-- MAGIC CREATE SCHEMA IF NOT EXISTS ccurated

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

-- MAGIC %%sql
-- MAGIC CREATE TABLE IF NOT EXISTS ccurated.dim_date (
-- MAGIC     OrderDate DATE,
-- MAGIC     Day INT,
-- MAGIC     Month INT,
-- MAGIC     Year INT,
-- MAGIC     mmmyyyy STRING,
-- MAGIC     yyyymm STRING
-- MAGIC );

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
