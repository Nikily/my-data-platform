"""
Daily pipeline schedule.

Runs the full pipeline (ingestion → dbt → export) once per day at 08:00 CET
(Europe/Paris timezone). Dagster handles the CET/CEST offset automatically —
the job will always fire at 08:00 local time regardless of daylight saving.
"""

from dagster import AssetSelection, ScheduleDefinition

daily_schedule = ScheduleDefinition(
    name="daily_pipeline",
    cron_schedule="0 8 * * *",          # 08:00 Europe/Paris every day
    execution_timezone="Europe/Paris",
    target=AssetSelection.all(),
    description=(
        "Runs all ingestion, transformation, and export assets daily at "
        "08:00 CET/CEST (Europe/Paris)."
    ),
)
