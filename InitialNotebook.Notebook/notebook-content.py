# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

from notebookutils import notebook, mssparkutils
import sempy.fabric as fabric

# Workspace-ID
workspace_id = spark.conf.get("trident.workspace.id")

# Lakehouse-ID abrufen
lakehouses = mssparkutils.lakehouse.list(workspaceId=workspace_id)
lakehouse_id = next(lh for lh in lakehouses if lh["displayName"] == "Blueprint_LH")["id"]

# Alle Notebooks abrufen
notebooks = fabric.list_items().query("Type == 'Notebook'")

# --- Ausschlussliste ---
exclude = ["InitialNotebook"]  # <- hier die Notebooks eintragen, die NICHT geändert werden sollen
notebooks = notebooks[~notebooks["Display Name"].isin(exclude)]

# (Optional) Check: welche werden aktualisiert?
print("Diese Notebooks werden aktualisiert:")
print(notebooks["Display Name"].tolist())

# Iteriere über alle (gefilterten) Notebooks und aktualisiere die Definition
for _, nb in notebooks.iterrows():
    nb_name = nb["Display Name"]
    print(f"Aktualisiere {nb_name}...")

    notebook.updateDefinition(
        name=nb_name,
        workspaceId=workspace_id,
        defaultLakehouse=lakehouse_id,
        defaultLakehouseWorkspace=workspace_id
    )

print("✅ Alle Notebook-Definitionen wurden aktualisiert.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%pip install semantic-link-labs 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from sempy_labs.directlake import update_direct_lake_model_lakehouse_connection
dataset_name = "Blueprint_SM"
lakehouse_name = "Blueprint_LH"
update_direct_lake_model_lakehouse_connection(dataset=dataset_name,lakehouse=lakehouse_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
