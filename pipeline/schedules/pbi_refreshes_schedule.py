"""
Power BI refresh-status hourly schedule.

Runs pbi_admin_refreshes_raw every hour to capture the latest refresh
attempt per semantic model, then updates the incremental refresh-status
intermediate model.

Kept separate from the daily pipeline to avoid hammering the PBI Admin API
unnecessarily for data that only changes when a dataset refresh completes.
"""

from dagster import AssetKey, AssetSelection, ScheduleDefinition

pbi_refreshes_schedule = ScheduleDefinition(
    name="hourly_pbi_refreshes",
    cron_schedule="0 * * * *",              # top of every hour
    execution_timezone="Europe/Paris",
    target=AssetSelection.assets(
        "pbi_admin_refreshes_raw",
        AssetKey(["staging", "stg_pbi_admin__dataset_refreshes"]),
        AssetKey(["intermediate", "int_pbi_admin__refresh_status"]),
    ),
    description=(
        "Fetches the latest refresh status for all refreshable semantic models "
        "hourly, materialises the staging view, then updates the incremental "
        "int_pbi_admin__refresh_status model."
    ),
)
