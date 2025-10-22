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

# #### Delta Load Stage Table

# CELL ********************

from pyspark.sql.functions import (
    current_timestamp, col, when, lit
)
from pyspark.sql.types import DecimalType
from pyspark.sql.functions import input_file_name

# 1. Read from raw layer
raw_df = spark.table("bronze.salesorder")

# 2. Apply transformations
stage_df = (
    raw_df
    .dropDuplicates(["SalesOrderNumber", "SalesOrderLineNumber"])
    .withColumn("Created", current_timestamp())
    .withColumn("IsFlagged", when(col("OrderDate") < '2019-08-01', True).otherwise(False))
    .withColumn("ModifiedTS", current_timestamp())
    .withColumn(
        "CustomerName",
        when(
            col("CustomerName").isNull() | (col("CustomerName") == ""), lit("Unknown")
        ).otherwise(col("CustomerName"))
    )
    # etc. 
)

# 3. Reorder columns to match the SQL table
ordered_cols = [
    "SalesOrderNumber",
    "SalesOrderLineNumber",
    "OrderDate",
    "CustomerName",
    "Email",
    "Item",
    "Quantity",
    "UnitPrice",
    "Tax",
    "source_file",
    "Created",
    "IsFlagged",
    "ModifiedTS"
]

stage_df = stage_df.select(*ordered_cols)

# 4. Write to stage layer table
stage_df.write.mode("overwrite").saveAsTable("silber.salesorder")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM silber.salesorder LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
