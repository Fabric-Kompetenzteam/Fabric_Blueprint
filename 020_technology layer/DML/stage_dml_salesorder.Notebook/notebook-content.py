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

# #### Delta Load Stage Table

# CELL ********************

from pyspark.sql.functions import (
    current_timestamp, col, when, lit
)
from pyspark.sql.types import DecimalType
from pyspark.sql.functions import input_file_name

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Read from raw layer
raw_df = spark.table("raw.salesorder")

# 2. Apply transformations
stage_df = (
    raw_df
    .dropDuplicates(["SalesOrderNumber", "SalesOrderLineNumber"])
    .withColumn("IsFlagged", when(col("OrderDate") < '2019-08-01', True).otherwise(False))
    .withColumn(
        "CustomerName",
        when(
            col("CustomerName").isNull() | (col("CustomerName") == ""), lit("Unknown")
        ).otherwise(col("CustomerName"))
    )
    .withColumn("__InsertTimestampStageUTC", current_timestamp())
    .withColumn("__ModifiedTimestampStageUTC", current_timestamp())
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
    "IsFlagged",
    "__SourceFile",
    "__InsertTimestampStageUTC",
    "__ModifiedTimestampStageUTC"
]

stage_df = stage_df.select(*ordered_cols)

# 4. Write to stage layer table
stage_df.write.mode("overwrite").saveAsTable("stage.salesorder")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
