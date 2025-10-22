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
# META           "id": "0bf803b2-9cd0-4488-96d3-add3c6124c8f"
# META         },
# META         {
# META           "id": "303765a9-18c4-4cb6-aad4-c827f21b831d"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## Imports

# CELL ********************

from pyspark.sql.functions import col, input_file_name
from pyspark.sql.types import DecimalType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Delta Load Raw Table

# CELL ********************

# 1. Define your column names
columns = [
    "SalesOrderNumber",
    "SalesOrderLineNumber",
    "OrderDate",
    "CustomerName",
    "Email",
    "Item",
    "Quantity",
    "UnitPrice",
    "Tax"
]

# 2. Read all CSV files (no headers)
df = spark.read.format("csv") \
    .option("header", "false") \
    .option("inferSchema", "true") \
    .load("Files/*.csv") \
    .toDF(*columns)

# 4. Add source file column for lineage
df = df.withColumn("source_file", input_file_name())

# 5. Optional: filter out accidental header rows (if any file has a header by mistake)
df = df.filter(col("SalesOrderLineNumber").cast("int").isNotNull())

# 6. Register DataFrame as a temp view
df.createOrReplaceTempView("staging_salesorder")

# Run Spark SQL MERGE (upsert)
spark.sql("""
MERGE INTO araw.salesorder AS target
USING staging_salesorder AS source
ON target.SalesOrderNumber = source.SalesOrderNumber
   AND target.SalesOrderLineNumber = source.SalesOrderLineNumber
WHEN MATCHED THEN
  UPDATE SET *
WHEN NOT MATCHED THEN
  INSERT *
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM araw.salesorder LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
