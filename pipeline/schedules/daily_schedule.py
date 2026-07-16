"""
Power BI Admin API daily ingestion schedule.

Fetches a fresh snapshot of all Power BI Admin API endpoints and runs the
Workspace Scanner so that the daily_pbi_intermediate schedule (05:00) has
up-to-date data to process.

Run order (Dagster respects asset deps automatically):
  1. pbi_admin_raw         — full snapshot: apps, capacities, refreshables,
                             groups, dashboards, reports, datasets,
                             widely-shared artifacts
  2. pbi_admin_scanner_raw — Workspace Scanner: metadata + datasource details
                             for all active non-personal workspaces (depends
                             on pbi_admin_raw)

Runs at 03:00 CET/CEST every day — two hours before daily_pbi_intermediate
fires at 05:00, giving the scanner time to complete across all workspace
batches.
"""

from dagster import AssetSelection, ScheduleDefinition

daily_schedule = ScheduleDefinition(
    name="daily_pbi_ingestion",
    cron_schedule="0 3 * * *",           # 03:00 Europe/Paris every day
    execution_timezone="Europe/Paris",
    target=AssetSelection.assets(
        "pbi_admin_raw",
        "pbi_admin_scanner_raw",
    ),
    description=(
        "Fetches a fresh Power BI Admin API snapshot and runs the Workspace "
        "Scanner daily at 03:00 CET/CEST, so daily_pbi_intermediate has "
        "up-to-date data when it fires at 05:00."
    ),
)
