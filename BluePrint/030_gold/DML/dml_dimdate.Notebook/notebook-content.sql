-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "ae307d1f-c19d-4a89-b373-3c58878cc08a",
-- META       "default_lakehouse_name": "Blueprint_LH",
-- META       "default_lakehouse_workspace_id": "1d8f6de1-70b1-4989-ac36-66143ee32cfd",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "ae307d1f-c19d-4a89-b373-3c58878cc08a"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- MARKDOWN ********************

-- #### Load Dim Date Table 

-- CELL ********************

CREATE OR REPLACE TABLE gold.dim_date AS
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
