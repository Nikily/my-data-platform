"""
Parquet export asset.

After dbt has finished transforming data, this asset reads each mart table
from DuckDB and uploads it as a Parquet file to Azure Blob Storage.

Power BI Service and Power BI Desktop connect to the Azure Blob container
using the native Azure Blob Storage connector — no gateway or ODBC driver
required.

HOW TO CUSTOMISE:
  1. Set AZURE_STORAGE_ACCOUNT_NAME, AZURE_TENANT_ID, AZURE_CLIENT_ID,
     AZURE_CLIENT_SECRET, EXPORT_CONTAINER and EXPORT_PATH in your .env file.
  2. Add the name of each dbt mart model you want to export to MART_TABLES.
  3. In Power BI, connect to Azure Blob Storage, point at EXPORT_CONTAINER,
     and load the Parquet files from EXPORT_PATH.

FILE NAMING:
  Each table is exported as:
    <EXPORT_PATH><table_name>.parquet
  e.g.  marts/dim_customer.parquet
        marts/fact_orders.parquet
"""

import io
import os

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dagster import AssetExecutionContext, asset

# ── Tables to export — (schema, table_name) ───────────────────────────────────
EXPORT_TABLES: list[tuple[str, str]] = [
    # Enriched CDR detail with site information — primary Power BI source
    ("main_intermediate", "int_8x8_cdr_enriched"),
]


def _export_table_to_blob(
    conn: duckdb.DuckDBPyConnection,
    blob_client: BlobServiceClient,
    schema: str,
    table: str,
    container: str,
    blob_prefix: str,
) -> int:
    """Reads a DuckDB table and uploads it as Parquet to Azure Blob Storage."""
    arrow_table: pa.Table = conn.execute(
        f"SELECT * FROM {schema}.{table};"
    ).fetch_arrow_table()

    buffer = io.BytesIO()
    pq.write_table(arrow_table, buffer, compression="snappy")
    buffer.seek(0)

    blob_name = f"{blob_prefix}{table}.parquet"
    blob_client.get_blob_client(container=container, blob=blob_name).upload_blob(
        buffer, overwrite=True
    )
    return len(arrow_table)


@asset(
    group_name="export",
    kinds={"duckdb", "azure"},
    description=(
        "Exports dbt mart tables from DuckDB as Parquet files to Azure Blob Storage "
        "so Power BI Service and Desktop can connect natively."
    ),
    deps=["dbt_models", "azure_container_export"],
)
def parquet_export(context: AssetExecutionContext) -> None:
    account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
    container = os.environ["EXPORT_CONTAINER"]
    blob_prefix = os.environ.get("EXPORT_PATH", "marts/")

    credential = ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
    )
    blob_service = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=credential,
    )

    with duckdb.connect(os.environ["DUCKDB_PATH"], read_only=True) as conn:
        for schema, table in EXPORT_TABLES:
            row_count = _export_table_to_blob(
                conn=conn,
                blob_client=blob_service,
                schema=schema,
                table=table,
                container=container,
                blob_prefix=blob_prefix,
            )
            context.log.info(
                f"Exported {row_count:,} rows → {blob_prefix}{table}.parquet"
            )
