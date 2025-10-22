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

DAG = {
    "activities": [
                {
            "name": "raw_dml", 
            "path": "raw_dml", 
            "timeoutPerCellInSeconds": 600,
        },
        {
            "name": "stage_dml", 
            "path": "stage_dml", 
            "timeoutPerCellInSeconds": 600,
             "dependencies": ["raw_dml"
                            ]
        },
        {
            "name": "curated_dml_dimcustomer", 
            "path": "curated_dml_dimcustomer", 
            "timeoutPerCellInSeconds": 600,
            "dependencies": ["stage_dml"
                            ]
        },
        {
            "name": "curated_dml_dimproduct", 
            "path": "curated_dml_dimproduct", 
            "timeoutPerCellInSeconds": 600,
            "dependencies": ["stage_dml"
                            ]
        },
        {
            "name": "curated_dml_factsales", 
            "path": "curated_dml_factsales", 
            "timeoutPerCellInSeconds": 600,
            "dependencies": ["curated_dml_dimcustomer",
                             "curated_dml_dimproduct"
                            ]
        }
    ],
    "timeoutInSeconds": 3600, # max 1 hour for the entire pipeline
    "concurrency": 5 # max 5 notebooks in parallel
}



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#check the API documentation for available DAG layouts, e.g. spring, circular, planar etc
mssparkutils.notebook.runMultiple(DAG, {"displayDAGViaGraphviz": False})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
