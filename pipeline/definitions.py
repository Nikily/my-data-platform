"""
Dagster Definitions — the top-level entry point for the data platform.

This file wires together all assets, resources, and schedules.
`pyproject.toml` points `dagster dev` / `dagster-webserver` at this module
via the `[tool.dagster] module_name` setting.
"""

from pathlib import Path

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_duckdb import DuckDBResource

from pipeline.assets.export import parquet_export
from pipeline.assets.sources import adls_delta, csv_local, csv_sftp, eight_x_eight_cdr, rest_api
from pipeline.schedules.daily_schedule import daily_schedule

# ── dbt project setup ─────────────────────────────────────────────────────────
# DbtProject manages the lifecycle of the dbt project.
# `prepare_if_dev()` runs `dbt parse` on startup to generate manifest.json
# when running locally / in development. In production the manifest should be
# pre-compiled as part of your deploy step (run `dbt parse` before starting the
# Dagster services).
DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_project"

dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
dbt_project.prepare_if_dev()


@dbt_assets(
    manifest=dbt_project.manifest_path,
    name="dbt_models",
)
def dbt_models(context, dbt: DbtCliResource):
    """Runs all dbt models (staging → marts)."""
    yield from dbt.cli(["run"], context=context).stream()


# ── Collect all assets ────────────────────────────────────────────────────────
ingestion_assets = load_assets_from_modules([rest_api, csv_local, csv_sftp, adls_delta, eight_x_eight_cdr])
export_assets = load_assets_from_modules([parquet_export])

# ── Definitions ───────────────────────────────────────────────────────────────
defs = Definitions(
    assets=[
        *ingestion_assets,
        dbt_models,
        *export_assets,
    ],
    resources={
        # Shared DuckDB connection — used by ADLS Delta source and Parquet export.
        # dlt and dbt manage their own connections to the same file via DUCKDB_PATH.
        "duckdb": DuckDBResource(database="${DUCKDB_PATH}"),

        # dbt CLI resource — points at our dbt project and profiles directory.
        "dbt": DbtCliResource(
            project_dir=str(DBT_PROJECT_DIR),
            profiles_dir=str(DBT_PROJECT_DIR),
        ),
    },
    schedules=[daily_schedule],
)
