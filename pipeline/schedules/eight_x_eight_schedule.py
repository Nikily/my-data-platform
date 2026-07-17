"""
8x8 daily pipeline schedule.

Runs only the assets needed for the 8x8 CDR pipeline in dependency order:
  1. azure_container_8x8        — ensure raw container exists
  2. eight_x_eight_cdr_raw      — ingest CDR from 8x8 API into DuckDB
  3. dbt models                 — stage + enrich (stg_cdr → int_cdr_enriched)
  4. azure_container_export     — ensure export container exists
  5. parquet_export             — write Parquet to Azure Blob Storage

Runs daily at 07:00 CET/CEST (Europe/Paris).
"""

from dagster import AssetKey, AssetSelection, ScheduleDefinition

eight_x_eight_schedule = ScheduleDefinition(
    name="daily_eight_x_eight",
    cron_schedule="0 7,14 * * *",          # 07:00 Europe/Paris every day
    execution_timezone="Europe/Paris",
    target=AssetSelection.assets(
        "azure_container_8x8",
        "eight_x_eight_cdr_raw",
        AssetKey(["staging", "stg_8x8_call_detail_records"]),
        AssetKey(["intermediate", "int_8x8_cdr_enriched"]),
        "azure_container_export",
        "parquet_export",
    ),
    description=(
        "Runs the 8x8 CDR ingestion, dbt transformation, and Parquet export "
        "daily at 07:00 and 14:00 CET/CEST."
    ),
)
