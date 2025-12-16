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

# ## Imports

# CELL ********************

from pyspark.sql.functions import col, input_file_name, current_timestamp
from pyspark.sql.types import DecimalType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Workspace-ID
workspace_id = spark.conf.get("trident.workspace.id")
# Lakehouse-ID
lakehouse_id = spark.conf.get("trident.lakehouse.id")

# Basis-Pfad zum CSV-Ordner
base_path = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Files/010 - Raw/*"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

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

try:
    # Alle CSV-Dateien im Ordner einlesen
    raw_df = (spark.read.format("csv")
              .option("header", "false")  # Wenn CSVs Header haben
              .option("inferSchema", "true")  # Schema automatisch erkennen
              .load(base_path)
              .toDF(*columns)
             )

    print(f"Anzahl geladener Datensätze: {raw_df.count()}")
except Exception as e:
    raise SystemExit(f"Fehler beim Laden der CSV-Dateien: {e}")

# 4. Add source file column for lineage
raw_df = raw_df.withColumn("__SourceFile", input_file_name()) \
               .withColumn("__InsertTimestampRawUTC", current_timestamp())

# 5. Optional: filter out accidental header rows (if any file has a header by mistake)
raw_df = raw_df.filter(col("SalesOrderLineNumber").cast("int").isNotNull())

# 6. Register DataFrame as a temp view
raw_df.createOrReplaceTempView("staging_salesorder")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Delta Load Raw Table

# CELL ********************

# Run Spark SQL MERGE (upsert)
spark.sql("""
MERGE INTO raw.salesorder AS tgt
USING staging_salesorder AS src
ON tgt.SalesOrderNumber = src.SalesOrderNumber
   AND tgt.SalesOrderLineNumber = src.SalesOrderLineNumber
WHEN MATCHED THEN
  UPDATE SET
        tgt.OrderDate = src.OrderDate,
        tgt.CustomerName = src.CustomerName,
        tgt.Email = src.Email,
        tgt.Item = src.Item,
        tgt.Quantity = src.Quantity,
        tgt.UnitPrice = src.UnitPrice,
        tgt.Tax = src.Tax,        
        tgt.__SourceFile = src.__SourceFile,
        tgt.__InsertTimestampRawUTC = src.__InsertTimestampRawUTC
WHEN NOT MATCHED THEN
  INSERT (
        SalesOrderNumber,
        SalesOrderLineNumber,
        OrderDate,
        CustomerName,
        Email,
        Item,
        Quantity,
        UnitPrice,
        Tax,
        __SourceFile,
        __InsertTimestampRawUTC
  )
  VALUES(
        src.SalesOrderNumber,
        src.SalesOrderLineNumber,
        src.OrderDate,
        src.CustomerName,
        src.Email,
        src.Item,
        src.Quantity,
        src.UnitPrice,
        src.Tax,
        src.__SourceFile,
        src.__InsertTimestampRawUTC
  )
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
