"""
Dagster Definitions — the top-level entry point for the data platform.

This file wires together all assets, resources, and schedules.
`pyproject.toml` points `dagster dev` / `dagster-webserver` at this module
via the `[tool.dagster] module_name` setting.
"""

import sys
from pathlib import Path

from dagster import AssetKey, Definitions, EnvVar, load_assets_from_modules
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, DbtProject, dbt_assets
from dagster_duckdb import DuckDBResource

from pipeline.assets.export import parquet_export
from pipeline.assets.infra import azure_containers
from pipeline.assets.sources import adls_delta, csv_local, csv_sftp, eight_x_eight_cdr, eight_x_eight_users, pbi_admin, rest_api
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


class _DbtTranslator(DagsterDbtTranslator):
    """Maps the raw_eight_x_eight.call_detail_records dbt source to the
    eight_x_eight_cdr_raw Dagster asset so Dagster enforces execution order
    and does not run ingestion and dbt in parallel (which causes a DuckDB lock conflict)."""

    def get_asset_key(self, dbt_resource_props: dict) -> AssetKey:
        resource_type = dbt_resource_props.get("resource_type")
        source_name   = dbt_resource_props.get("source_name")
        table_name    = dbt_resource_props.get("name")

        if resource_type == "source":
            # Map the canonical 8x8 CDR source to its Dagster asset so dbt
            # waits for ingestion before running (prevents DuckDB lock conflicts).
            if source_name == "raw_eight_x_eight" and table_name == "call_detail_records":
                return AssetKey("eight_x_eight_cdr_raw")

            # Map the canonical PBI Admin source to its Dagster asset.
            if source_name == "raw_pbi_admin" and table_name == "apps":
                return AssetKey("pbi_admin_raw")

        return super().get_asset_key(dbt_resource_props)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    name="dbt_models",
    dagster_dbt_translator=_DbtTranslator(),
)
def dbt_models(context, dbt: DbtCliResource):
    """Runs all dbt models (staging → marts)."""
    yield from dbt.cli(["run"], context=context).stream()


# ── Collect all assets ────────────────────────────────────────────────────────
infra_assets = load_assets_from_modules([azure_containers])
ingestion_assets = load_assets_from_modules([rest_api, csv_local, csv_sftp, adls_delta, eight_x_eight_cdr, eight_x_eight_users, pbi_admin])
# pbi_admin exports both pbi_admin_raw and pbi_admin_unused_artifacts_raw
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
