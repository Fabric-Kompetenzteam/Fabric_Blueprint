# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ae307d1f-c19d-4a89-b373-3c58878cc08a",
# META       "default_lakehouse_name": "Blueprint_LH",
# META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
# META       "known_lakehouses": [
# META         {
# META           "id": "ae307d1f-c19d-4a89-b373-3c58878cc08a"
# META         }
# META       ]
# META     }
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
    split(CustomerName, ' ')[0] AS First,
    CASE WHEN size(split(CustomerName, ' ')) > 1 THEN split(CustomerName, ' ')[1] ELSE '' END AS Last
FROM silber.salesorder
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

# MAGIC %%sql
# MAGIC SELECT * FROM source_delta_dfdistinct_customers LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Creating Temp View Max ID 
source_delta_df = spark.sql(f"""
SELECT COALESCE(MAX(CustomerID), 0) AS max_id
FROM gold.dim_customer
""")
source_delta_df.createOrReplaceTempView(f"source_delta_dfmax_id_view")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Number the new records with offset
# MAGIC WITH numbered_customers AS (
# MAGIC   SELECT 
# MAGIC     dc.CustomerName, 
# MAGIC     dc.Email, 
# MAGIC     dc.First, 
# MAGIC     dc.Last,
# MAGIC     (ROW_NUMBER() OVER (ORDER BY dc.Email) + miv.max_id) AS CustomerID
# MAGIC   FROM source_delta_dfdistinct_customers dc
# MAGIC   CROSS JOIN source_delta_dfmax_id_view miv
# MAGIC   LEFT ANTI JOIN gold.dim_customer t
# MAGIC     ON dc.Email = t.Email
# MAGIC )
# MAGIC 
# MAGIC -- Merge new data with existing data 
# MAGIC MERGE INTO gold.dim_customer AS target
# MAGIC USING numbered_customers AS source
# MAGIC ON target.Email = source.Email
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT (CustomerID, CustomerName, Email, FirstName, LastName)
# MAGIC   VALUES (source.CustomerID, source.CustomerName, source.Email, source.First, source.Last);


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM gold.dim_customer LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
