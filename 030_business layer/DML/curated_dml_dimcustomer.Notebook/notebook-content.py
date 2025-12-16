# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "555cd4d6-87bd-49c3-b473-7e83cb83f1eb",
# META       "default_lakehouse_name": "Blueprint_LH",
# META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
# META       "known_lakehouses": [
# META         {
# META           "id": "b52127d0-485c-4fb0-b7ee-b8d80858f144"
# META         },
# META         {
# META           "id": "555cd4d6-87bd-49c3-b473-7e83cb83f1eb"
# META         }
# META       ]
# META     },
# META     "environment": {}
# META   }
# META }

# MARKDOWN ********************

# #### Delta Load Dim Customer Table

# CELL ********************

# Creating Temp View with distinct customers from stage table 
source_delta_df = spark.sql(f"""
    SELECT
    CustomerName,
    Email,
    split(CustomerName, ' ')[0] AS FirstName,
    CASE WHEN size(split(CustomerName, ' ')) > 1 THEN split(CustomerName, ' ')[1] ELSE '' END AS LastName
FROM stage.salesorder
WHERE CustomerName IS NOT NULL AND Email IS NOT NULL
GROUP BY CustomerName, Email
""")
source_delta_df.createOrReplaceTempView(f"source_delta_dfdistinct_customers")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Creating Temp View Max ID 
source_delta_df = spark.sql(f"""
SELECT COALESCE(MAX(CustomerID), 0) AS max_id
FROM curated.dim_customer
""")
source_delta_df.createOrReplaceTempView(f"source_delta_dfmax_id_view")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC WITH new_customers AS (
# MAGIC   SELECT 
# MAGIC       (ROW_NUMBER() OVER (ORDER BY dc.Email) + miv.max_id) AS CustomerID,
# MAGIC       dc.CustomerName,
# MAGIC       dc.Email,
# MAGIC       dc.FirstName,
# MAGIC       dc.LastName      
# MAGIC   FROM source_delta_dfdistinct_customers dc
# MAGIC   CROSS JOIN source_delta_dfmax_id_view miv
# MAGIC   LEFT ANTI JOIN curated.dim_customer t
# MAGIC     ON dc.Email = t.Email
# MAGIC ),
# MAGIC existing_customers AS (
# MAGIC   SELECT
# MAGIC       t.CustomerID,                 
# MAGIC       dc.CustomerName,
# MAGIC       dc.Email,
# MAGIC       dc.FirstName,
# MAGIC       dc.LastName
# MAGIC   FROM source_delta_dfdistinct_customers dc
# MAGIC   INNER JOIN curated.dim_customer t
# MAGIC     ON dc.Email = t.Email
# MAGIC ),
# MAGIC source_union AS (
# MAGIC   SELECT * FROM new_customers
# MAGIC   UNION ALL
# MAGIC   SELECT * FROM existing_customers
# MAGIC )
# MAGIC 
# MAGIC MERGE INTO curated.dim_customer AS target
# MAGIC USING source_union AS source
# MAGIC ON target.Email = source.Email
# MAGIC 
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     target.CustomerName = source.CustomerName,
# MAGIC     target.FirstName    = source.FirstName,
# MAGIC     target.LastName     = source.LastName
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT (CustomerID, CustomerName, Email, FirstName, LastName)
# MAGIC   VALUES (source.CustomerID, source.CustomerName, source.Email, source.FirstName, source.LastName)

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
