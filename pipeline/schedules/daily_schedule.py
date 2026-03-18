"""
Daily pipeline schedule.

Runs the full pipeline (ingestion → dbt → export) once per day at 02:00 UTC.
Adjust the cron expression to suit your preferred run time.
"""

from dagster import AssetSelection, ScheduleDefinition

daily_schedule = ScheduleDefinition(
    name="daily_pipeline",
    cron_schedule="0 2 * * *",  # 02:00 UTC every day
    target=AssetSelection.all(),
    description="Runs all ingestion, transformation, and export assets daily at 02:00 UTC.",
)
