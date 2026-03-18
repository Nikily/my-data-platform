"""
Azure Data Lake / OneLake Delta table ingestion asset.

Reads Delta tables written by Fabric Link (or Synapse Link) for Dataverse
directly into DuckDB using DuckDB's native `azure` and `delta` extensions.
No dlt required — DuckDB handles the Delta transaction log and incremental
file reads natively.

HOW TO CUSTOMISE:
  1. Set AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_ACCOUNT_KEY,
     ADLS_CONTAINER and ADLS_DELTA_PATH in your .env file.
  2. Add one function per Dataverse entity (table) you want to ingest,
     following the pattern of `ingest_delta_table` below.
  3. Adjust dataset_name and table_name to reflect your entity structure.

PREREQUISITE:
  Fabric Link (or Synapse Link) for Dataverse must be enabled by your Azure
  administrator. The Delta table path on ADLS Gen2 / OneLake is typically:
    az://<container>/<entity_name>/

NOTE ON INCREMENTAL LOADING:
  DuckDB's delta extension reads the Delta transaction log and only scans
  Parquet files added since the last checkpoint. Full-table replacement
  (CREATE OR REPLACE) is used here for simplicity and correctness at low
  volume. For larger tables, switch to an incremental merge using a
  watermark column.
"""

import os

import duckdb
from dagster import AssetExecutionContext, asset


def _configure_azure(conn: duckdb.DuckDBPyConnection) -> None:
    """Install and configure DuckDB azure + delta extensions."""
    conn.execute("INSTALL azure; LOAD azure;")
    conn.execute("INSTALL delta; LOAD delta;")
    conn.execute(
        f"""
        CREATE SECRET IF NOT EXISTS azure_secret (
            TYPE AZURE,
            ACCOUNT_NAME '{os.environ["AZURE_STORAGE_ACCOUNT_NAME"]}',
            ACCOUNT_KEY  '{os.environ["AZURE_STORAGE_ACCOUNT_KEY"]}'
        );
        """
    )


def ingest_delta_table(
    conn: duckdb.DuckDBPyConnection,
    container: str,
    delta_path: str,
    target_schema: str,
    target_table: str,
) -> int:
    """
    Reads a Delta table from ADLS Gen2 into a DuckDB table.
    Returns the number of rows loaded.
    """
    delta_url = f"az://{container}/{delta_path}"

    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {target_schema};")
    conn.execute(
        f"""
        CREATE OR REPLACE TABLE {target_schema}.{target_table} AS
        SELECT * FROM delta_scan('{delta_url}');
        """
    )
    result = conn.execute(
        f"SELECT COUNT(*) FROM {target_schema}.{target_table};"
    ).fetchone()
    return result[0] if result else 0


@asset(
    group_name="raw_ingestion",
    kinds={"duckdb", "azure"},
    description=(
        "Reads Dataverse entities from Delta tables on ADLS Gen2 / OneLake "
        "into DuckDB (raw layer) using DuckDB's native azure + delta extensions."
    ),
)
def adls_delta_raw(context: AssetExecutionContext) -> None:
    container = os.environ["ADLS_CONTAINER"]
    delta_path = os.environ["ADLS_DELTA_PATH"]

    with duckdb.connect(os.environ["DUCKDB_PATH"]) as conn:
        _configure_azure(conn)

        # ── Add one call per Dataverse entity you want to ingest ──────────────
        # ingest_delta_table(conn, container, "Tables/account",  "raw_dataverse", "account")
        # ingest_delta_table(conn, container, "Tables/contact",  "raw_dataverse", "contact")
        # ingest_delta_table(conn, container, "Tables/incident", "raw_dataverse", "incident")

        row_count = ingest_delta_table(
            conn,
            container=container,
            delta_path=delta_path,
            target_schema="raw_dataverse",
            target_table="entity",  # rename to match the actual entity
        )

    context.log.info(f"Loaded {row_count:,} rows from Delta table at {delta_path}")
