-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "303765a9-18c4-4cb6-aad4-c827f21b831d",
-- META       "default_lakehouse_name": "plansee_lh",
-- META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "303765a9-18c4-4cb6-aad4-c827f21b831d"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- MARKDOWN ********************

-- #### Load Dim Date Table 

-- CELL ********************

CREATE OR REPLACE TABLE ccurated.dim_date AS
SELECT
    d AS OrderDate,
    day(d)   AS Day,
    month(d) AS Month,
    year(d)  AS Year,
    date_format(d, 'MMM-yyyy') AS mmmyyyy,
    date_format(d, 'yyyyMM')   AS yyyymm,
    dayofweek(d) AS DayOfWeek,
    weekofyear(d) AS WeekOfYear,
    CASE WHEN dayofweek(d) IN (1,7) THEN True ELSE False END AS IsWeekend
FROM (
    SELECT explode(sequence(
        to_date('2018-01-01'),
        to_date('2050-12-31'),
        interval 1 day
    )) AS d
) tmp
ORDER BY OrderDate;


-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

-- MAGIC %%pyspark
-- MAGIC df = spark.sql("SELECT * FROM plansee_lh.ccurated.dim_date LIMIT 10")
-- MAGIC display(df)

-- METADATA ********************

-- META {
-- META   "language": "python",
-- META   "language_group": "synapse_pyspark"
-- META }
