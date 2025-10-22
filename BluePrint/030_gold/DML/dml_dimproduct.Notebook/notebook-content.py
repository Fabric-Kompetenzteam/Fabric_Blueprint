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

# #### Delta Load Dim Product Table

# CELL ********************

# Creating Temp View with new or changed product info from stage table 
source_delta_df = spark.sql(f"""
SELECT
    dp.ItemName,
    dp.ItemInfo
FROM (
    SELECT DISTINCT
        split(Item, ', ')[0] AS ItemName,
        CASE 
            WHEN size(split(Item, ', ')) > 1 THEN split(Item, ', ')[1]
            ELSE ''
        END AS ItemInfo
    FROM silber.salesorder
    WHERE Item IS NOT NULL
) dp
LEFT JOIN (
    SELECT *
    FROM gold.dim_product
    WHERE IsCurrent = TRUE
) d
    ON dp.ItemName = d.ItemName
    AND dp.ItemInfo = d.ItemInfo
WHERE
    d.ItemName IS NULL -- New product
    OR dp.ItemInfo <> d.ItemInfo -- Changed product info
;
""")
source_delta_df.createOrReplaceTempView(f"source_delta_dfchanged_or_new_products")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM source_delta_dfchanged_or_new_products limit 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC --  End-date old product rows (for changed products) 
# MAGIC MERGE INTO gold.dim_product AS target
# MAGIC USING source_delta_dfchanged_or_new_products AS source
# MAGIC ON target.ItemName = source.ItemName AND target.IsCurrent = TRUE
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET target.ValidTo = current_timestamp(), target.IsCurrent = FALSE;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Insert new SCD2 product records with running ItemID
# MAGIC INSERT INTO gold.dim_product (
# MAGIC     ItemID,
# MAGIC     ItemName,
# MAGIC     ItemInfo,
# MAGIC     ValidFrom,
# MAGIC     ValidTo,
# MAGIC     IsCurrent
# MAGIC )
# MAGIC SELECT
# MAGIC     row_number() OVER (ORDER BY ItemName, ItemInfo) + (
# MAGIC         SELECT COALESCE(MAX(ItemID), 0) FROM gold.dim_product
# MAGIC     ) AS ItemID,
# MAGIC     ItemName,
# MAGIC     ItemInfo,
# MAGIC     current_timestamp() AS ValidFrom,
# MAGIC     NULL AS ValidTo,
# MAGIC     TRUE AS IsCurrent
# MAGIC FROM source_delta_dfchanged_or_new_products;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM gold.dim_product LIMIT(10)

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
