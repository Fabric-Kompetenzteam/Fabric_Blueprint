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

# #### Delta Load Dim Product Table

# CELL ********************

# Creating Temp View with new or changed product info from stage table 
source_delta_df = spark.sql(f"""
SELECT DISTINCT
    split(Item, ', ')[0] AS ItemName,
    CASE 
        WHEN size(split(Item, ', ')) > 1 THEN split(Item, ', ')[1]
        ELSE ''
    END AS ItemInfo
FROM stage.salesorder

""")
source_delta_df.createOrReplaceTempView(f"source_delta_dfchanged_or_new_products")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC MERGE INTO curated.dim_product AS t
# MAGIC USING (
# MAGIC   SELECT 
# MAGIC       s.ItemName,
# MAGIC       s.ItemInfo,
# MAGIC       ROW_NUMBER() OVER (ORDER BY s.ItemName) 
# MAGIC         + COALESCE((SELECT MAX(ItemID) FROM curated.dim_product), 0) AS NewItemID
# MAGIC   FROM source_delta_dfchanged_or_new_products s
# MAGIC ) AS s
# MAGIC ON t.ItemName = s.ItemName
# MAGIC AND t.ItemInfo = s.ItemInfo
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT (ItemID, ItemName, ItemInfo)
# MAGIC   VALUES (s.NewItemID, s.ItemName, s.ItemInfo);

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
