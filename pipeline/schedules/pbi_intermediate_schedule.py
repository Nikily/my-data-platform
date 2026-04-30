"""
Power BI intermediate layer daily schedule.

Materialises all five dbt models in the Power BI intermediate schema
after the main daily ingestion pipeline (which runs at 08:00) has had
time to complete. Runs at 10:00 CET/CEST every day.

Models materialised:
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
        AssetKey(["intermediate", "int_pbi_admin__reports"]),
        AssetKey(["intermediate", "int_pbi_admin__semantic_model_datasources"]),
        AssetKey(["intermediate", "int_pbi_admin__refresh_status"]),
        AssetKey(["intermediate", "int_pbi_admin__report_access"]),
        AssetKey(["intermediate", "int_pbi_admin__semantic_model_access"]),
    ),
    description=(
        "Materialises all Power BI intermediate dbt models daily at 10:00 CET/CEST, "
        "after the 08:00 ingestion pipeline (pbi_admin_raw + pbi_admin_scanner_raw) "
        "has had time to complete."
    ),
)
