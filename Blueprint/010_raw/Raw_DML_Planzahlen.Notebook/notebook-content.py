# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "1e2da8f0-e2e7-47a9-a9f6-2eec9f89205c",
# META       "default_lakehouse_name": "LH_Platform",
# META       "default_lakehouse_workspace_id": "c0a9d4d3-dd21-4ec5-b682-d591475e574b"
# META     },
# META     "environment": {
# META       "environmentId": "d1ee433e-0dd7-45b0-a36e-395c33731fb0",
# META       "workspaceId": "c0a9d4d3-dd21-4ec5-b682-d591475e574b"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # DML for raw.Planzahlen

# MARKDOWN ********************

# # Initialize base settings

# MARKDOWN ********************

# Import Libraries for notebook functions

# CELL ********************

import datetime
from pyspark.sql.functions import current_timestamp, regexp_extract, input_file_name, col

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.conf.set("environment", "dev")
spark.conf.set("raw.layer", "raw")
spark.conf.set("stage.layer", "stage")
spark.conf.set("core.layer", "core")
spark.conf.set("curated.layer", "curated")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Set the environment variables

# CELL ********************

# DBTITLE 1,Get variable values
raw_layer = spark.conf.get("raw.layer", "raw")
stage_layer = spark.conf.get("stage.layer", "stage")
core_layer = spark.conf.get("core.layer", "core")
curated_layer = spark.conf.get("curated.layer", "curated")
env = spark.conf.get("environment")
workspace_id = spark.conf.get("trident.workspace.id")
lakehouse_id = spark.conf.get("trident.lakehouse.id")

# static values
MAX_VALID_TO_DATE = "2999-12-31"
data_product = "intern"
data_module = "starpool"
table_name = "planzahlen"
full_table_name = "%s_%s_%s" % (data_product, data_module, table_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Read from Drop-Zone

# CELL ********************

from pyspark.sql.functions import input_file_name, current_timestamp

# Basis-Pfad zum CSV-Ordner
base_path = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Files/Planzahlen"

try:
    # Alle CSV-Dateien im Ordner einlesen
    raw_df = (spark.read
              .option("header", "true")  # Wenn CSVs Header haben
              .option("delimiter", ";")  # Delimiter auf Semikolon gesetzt
              .option("inferSchema", "true")  # Schema automatisch erkennen
              .csv(base_path)
              .withColumn("__file_name", input_file_name())
              .withColumn("__InsertTimestampRawUTC", current_timestamp())
             )

    print(f"Anzahl geladener Datensätze: {raw_df.count()}")
except Exception as e:
    raise SystemExit(f"Fehler beim Laden der CSV-Dateien: {e}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Write to RAW

# MARKDOWN ********************

# ## Enforce data types
# * Enforce data types
# * Identify records with non enforcable data types

# CELL ********************

raw_df.createOrReplaceTempView(f"raw_df{table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

raw_df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

typed_table_df = spark.sql(
    f"""
SELECT
    -- Table columns
    TRY_CAST(`Plakettenname1 Plan` AS STRING) AS Plakettenname1Plan,
    TRY_CAST(`Obervertrieb EP2ID Plan` AS STRING) AS ObervertriebEP2IDPlan,
    TRY_CAST(`Planzahl` AS STRING) AS Planzahl,
    TRY_CAST(`Planjahr` AS STRING) AS Planjahr,
    TRY_CAST(`Produktkategorie Plan` AS STRING) AS ProduktkategoriePlan,
    TRY_CAST(`Produktanbieter Kategorie Plan` AS STRING) AS ProduktanbieterKategoriePlan,

    -- Technical columns
    __file_name,
    CAST(current_timestamp() AS TIMESTAMP) AS __InsertTimestampRawUTC
FROM raw_df{table_name}
"""
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Beispiel ohne Anführungszeichen im Pfad
delta_table_path = f"Tables/{raw_layer}/{full_table_name}"  # Pfad ohne zusätzliche Anführungszeichen
# Schreiben in Delta-Tabelle
typed_table_df.write.format("delta").mode("overwrite").save(delta_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
