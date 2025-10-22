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

-- #### Delta Load Fact Table 

-- CELL ********************

-- Load unique transactions from stage table 
INSERT INTO gold.fact_sales (CustomerID, ItemID, OrderDate, Quantity, UnitPrice, Tax)
SELECT
    dc.CustomerID,
    dp.ItemID,
    s.OrderDate,
    s.Quantity,
    s.UnitPrice,
    s.Tax
FROM silber.salesorder s
JOIN gold.dim_customer dc
    ON s.CustomerName = dc.CustomerName AND s.Email = dc.Email
JOIN gold.dim_product dp
    ON split(s.Item, ', ')[0] = dp.ItemName
       AND
       CASE
           WHEN size(split(s.Item, ', ')) > 1 THEN split(s.Item, ', ')[1]
           ELSE ''
       END = dp.ItemInfo
WHERE s.CustomerName IS NOT NULL AND s.Email IS NOT NULL AND s.Item IS NOT NULL;


-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

SELECT * FROM gold.fact_sales LIMIT 10

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
