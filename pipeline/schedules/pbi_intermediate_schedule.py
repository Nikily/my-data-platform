"""
Power BI intermediate layer daily schedule.

Materialises the scanner staging views and all five intermediate dbt models.
Including the staging layer ensures the views always exist in DuckDB before
the intermediate models reference them — regardless of whether the manual
staging backfill has been run.

Runs at 10:00 CET/CEST every day, after the 08:00 ingestion pipeline.

Staging models materialised (scanner source, all have adapter.get_relation guard):
  - stg_pbi_admin__scanner_workspaces
  - stg_pbi_admin__scanner_reports
  - stg_pbi_admin__scanner_report_users
  - stg_pbi_admin__scanner_datasets
  - stg_pbi_admin__scanner_dataset_users
  - stg_pbi_admin__scanner_datasets__datasource_usages
  - stg_pbi_admin__scanner_datasource_instances

Intermediate models materialised:
  - int_pbi_admin__reports
  - int_pbi_admin__semantic_model_datasources
  - int_pbi_admin__refresh_status
  - int_pbi_admin__report_access
  - int_pbi_admin__semantic_model_access
"""

from dagster import AssetKey, AssetSelection, ScheduleDefinition

pbi_intermediate_schedule = ScheduleDefinition(
    name="daily_pbi_intermediate",
    cron_schedule="0 10 * * *",             # 10:00 Europe/Paris every day
    execution_timezone="Europe/Paris",
    target=AssetSelection.assets(
        # Scanner staging views — dependencies of the intermediate models.
        # Included here so they are always (re)created in the correct DuckDB
        # file before the intermediate models reference them.
        AssetKey(["staging", "stg_pbi_admin__scanner_workspaces"]),
        AssetKey(["staging", "stg_pbi_admin__scanner_reports"]),
        AssetKey(["staging", "stg_pbi_admin__scanner_report_users"]),
        AssetKey(["staging", "stg_pbi_admin__scanner_datasets"]),
        AssetKey(["staging", "stg_pbi_admin__scanner_dataset_users"]),
        AssetKey(["staging", "stg_pbi_admin__scanner_datasets__datasource_usages"]),
        AssetKey(["staging", "stg_pbi_admin__scanner_datasource_instances"]),
        # Intermediate models.
        AssetKey(["intermediate", "int_pbi_admin__reports"]),
        AssetKey(["intermediate", "int_pbi_admin__semantic_model_datasources"]),
        AssetKey(["intermediate", "int_pbi_admin__refresh_status"]),
        AssetKey(["intermediate", "int_pbi_admin__report_access"]),
        AssetKey(["intermediate", "int_pbi_admin__semantic_model_access"]),
    ),
    description=(
        "Materialises scanner staging views then all Power BI intermediate dbt models "
        "daily at 10:00 CET/CEST, after the 08:00 ingestion pipeline has completed."
    ),
)
