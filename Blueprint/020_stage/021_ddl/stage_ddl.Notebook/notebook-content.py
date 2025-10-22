# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "303765a9-18c4-4cb6-aad4-c827f21b831d",
# META       "default_lakehouse_name": "plansee_lh",
# META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
# META       "known_lakehouses": [
# META         {
# META           "id": "303765a9-18c4-4cb6-aad4-c827f21b831d"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# #### Creating Stage Table

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE SCHEMA IF NOT EXISTS bstage

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ###### Schema Stage Table

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE IF NOT EXISTS bstage.salesorder (
# MAGIC     SalesOrderNumber      STRING,
# MAGIC     SalesOrderLineNumber  INT,
# MAGIC     OrderDate             DATE,
# MAGIC     CustomerName          STRING,
# MAGIC     Email                 STRING,
# MAGIC     Item                  STRING,
# MAGIC     Quantity              INT,
# MAGIC     UnitPrice             DECIMAL(18, 2),
# MAGIC     Tax                   DECIMAL(18, 2),
# MAGIC     source_file           STRING,
# MAGIC     CREATED               TIMESTAMP,      -- Addtional system columns 
# MAGIC     IsFlagged             BOOLEAN,
# MAGIC     ModifiedTS            TIMESTAMP
# MAGIC )

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
