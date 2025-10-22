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
# META           "id": "303765a9-18c4-4cb6-aad4-c827f21b831d"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

file_paths = [
    'Files/010 - Raw/2019.csv',
    'Files/010 - Raw/2020.csv',
    'Files/010 - Raw/2021.csv'
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for file_path in file_paths:
    file_name = file_path.split('/')[-1]   # Extract the file name from the path
    print(f"=== {file_name} ===")
    df = spark.read.format("csv") \
        .option("header", "false") \
        .option("inferSchema", "true") \
        .load(file_path)
    display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC spark.sql(f"""
# MAGIC CREATE TABLE IF NOT EXISTS 2019
# MAGIC (
# MAGIC     -- Table columns
# MAGIC     CustomerSID BIGINT GENERATED ALWAYS AS IDENTITY COMMENT 'Surrogate key',
# MAGIC     CustomerNo BIGINT NOT NULL COMMENT 'Business key',
# MAGIC     C2 INT,
# MAGIC     C3 DATE,
# MAGIC     FullName STRING NOT NULL,
# MAGIC     Email STRING NOT NULL,
# MAGIC     Product STRING,
# MAGIC     NumItems INT,
# MAGIC     Amount1 DECIMAL(18, 2),
# MAGIC     Amount2 DECIMAL(18, 2),
# MAGIC     CreatedDate TIMESTAMP NOT NULL
# MAGIC )
# MAGIC USING delta
# MAGIC """)

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
