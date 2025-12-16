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

# #### Delta Load Fact Table 

# CELL ********************

source_delta_df = spark.sql(f"""
WITH src AS (
  SELECT
    s.SalesOrderNumber,
    s.SalesOrderLineNumber,
    CAST(s.OrderDate AS DATE)                      AS OrderDt,
    s.CustomerName,
    s.Email,
    s.Item,
    split(s.Item, ', ')[0]                         AS ItemName,
    CASE WHEN size(split(s.Item, ', ')) > 1
         THEN split(s.Item, ', ')[1] ELSE '' END   AS ItemInfo,
    s.Quantity,
    s.UnitPrice,
    s.Tax
  FROM stage.salesorder s
  WHERE s.SalesOrderNumber     IS NOT NULL
    AND s.SalesOrderLineNumber IS NOT NULL
    AND s.Email                IS NOT NULL
    AND s.Item                 IS NOT NULL
)
SELECT
  dc.CustomerID,
  dp.ItemID,
  dd.DateID AS OrderDateID,
  src.SalesOrderNumber,
  src.SalesOrderLineNumber,
  src.Quantity,
  src.UnitPrice,
  src.Tax,

  sha2(concat_ws('|',
        src.SalesOrderNumber,
        CAST(src.SalesOrderLineNumber AS STRING),
        CAST(dc.CustomerID           AS STRING),
        CAST(dp.ItemID               AS STRING),
        CAST(dd.DateID               AS STRING)
      ), 256) AS FactKeyHash
FROM src
JOIN curated.dim_customer dc
  ON lower(trim(dc.Email)) = lower(trim(src.Email))
JOIN curated.dim_product dp
  ON dp.ItemName = src.ItemName
 AND dp.ItemInfo = src.ItemInfo
JOIN curated.dim_date dd
  ON dd.FullDate = src.OrderDt
""")
source_delta_df.createOrReplaceTempView("source_delta_dffact")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC MERGE INTO curated.fact_sales AS t
# MAGIC USING source_delta_dffact     AS s
# MAGIC ON  t.FactKeyHash = s.FactKeyHash
# MAGIC 
# MAGIC WHEN MATCHED THEN UPDATE SET
# MAGIC   t.CustomerID           = s.CustomerID,
# MAGIC   t.ItemID               = s.ItemID,
# MAGIC   t.OrderDateID          = s.OrderDateID,
# MAGIC   t.SalesOrderNumber     = s.SalesOrderNumber,
# MAGIC   t.SalesOrderLineNumber = s.SalesOrderLineNumber,
# MAGIC   t.Quantity             = s.Quantity,
# MAGIC   t.UnitPrice            = s.UnitPrice,
# MAGIC   t.Tax                  = s.Tax
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN INSERT (
# MAGIC   CustomerID,
# MAGIC   ItemID,
# MAGIC   OrderDateID,
# MAGIC   SalesOrderNumber,
# MAGIC   SalesOrderLineNumber,
# MAGIC   Quantity,
# MAGIC   UnitPrice,
# MAGIC   Tax,
# MAGIC   FactKeyHash
# MAGIC )
# MAGIC VALUES (
# MAGIC   s.CustomerID,
# MAGIC   s.ItemID,
# MAGIC   s.OrderDateID,
# MAGIC   s.SalesOrderNumber,
# MAGIC   s.SalesOrderLineNumber,
# MAGIC   s.Quantity,
# MAGIC   s.UnitPrice,
# MAGIC   s.Tax,
# MAGIC   s.FactKeyHash
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
