"""
Dagster Definitions — the top-level entry point for the data platform.

This file wires together all assets, resources, and schedules.
`pyproject.toml` points `dagster dev` / `dagster-webserver` at this module
via the `[tool.dagster] module_name` setting.
"""

import sys
from pathlib import Path

from dagster import Definitions, EnvVar, load_assets_from_modules
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_duckdb import DuckDBResource

from pipeline.assets.export import parquet_export
from pipeline.assets.infra import azure_containers
from pipeline.assets.sources import adls_delta, csv_local, csv_sftp, eight_x_eight_cdr, eight_x_eight_users, rest_api
from pipeline.schedules.daily_schedule import daily_schedule
from pipeline.schedules.eight_x_eight_schedule import eight_x_eight_schedule

# ── dbt project setup ─────────────────────────────────────────────────────────
DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_project"
# dbt lives in the same venv as Dagster — derive the path from sys.executable
# so it works regardless of whether `dbt` is on the system PATH.
DBT_EXECUTABLE = str(Path(sys.executable).parent / "dbt")

dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
# In dev mode this runs `dbt parse` to regenerate the manifest.
# In production (systemd) it is a no-op; run `dbt parse` once after deploy.
dbt_project.prepare_if_dev()


@dbt_assets(
    manifest=dbt_project.manifest_path,
    name="dbt_models",
)
def dbt_models(context, dbt: DbtCliResource):
    """Runs all dbt models (staging → marts)."""
    yield from dbt.cli(["run"], context=context).stream()


# ── Collect all assets ────────────────────────────────────────────────────────
infra_assets = load_assets_from_modules([azure_containers])
ingestion_assets = load_assets_from_modules([rest_api, csv_local, csv_sftp, adls_delta, eight_x_eight_cdr, eight_x_eight_users])
export_assets = load_assets_from_modules([parquet_export])

# ── Definitions ───────────────────────────────────────────────────────────────
defs = Definitions(
    assets=[
        *infra_assets,
        *ingestion_assets,
        dbt_models,
        *export_assets,
    ],
    resources={
        # Shared DuckDB connection — used by ADLS Delta source and Parquet export.
        # dlt and dbt manage their own connections to the same file via DUCKDB_PATH.
        "duckdb": DuckDBResource(database=EnvVar("DUCKDB_PATH")),

        # dbt CLI resource — points at our dbt project and profiles directory.
        "dbt": DbtCliResource(
            project_dir=str(DBT_PROJECT_DIR),
            profiles_dir=str(DBT_PROJECT_DIR),
            dbt_executable=DBT_EXECUTABLE,
        ),
    },
    schedules=[daily_schedule, eight_x_eight_schedule],
)
