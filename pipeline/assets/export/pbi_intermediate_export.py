"""
Power BI intermediate layer Parquet export.

After the daily_pbi_intermediate dbt models have run, this asset reads each
int_pbi_admin__* view from DuckDB and uploads it as a Parquet file to Azure
Blob Storage so Power BI Service / Desktop can connect natively.

FILE NAMING:
  Each view is exported as:
    <PBI_INTERMEDIATE_EXPORT_PATH><view_name>.parquet
  e.g.  pbi_admin/int_pbi_admin__reports.parquet
"""

import io
import os

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dagster import AssetExecutionContext, AssetKey, asset

# Views to export — all are in the main_intermediate schema.
_PBI_INTERMEDIATE_VIEWS: list[str] = [
    "int_pbi_admin__reports",
    "int_pbi_admin__semantic_model_datasources",
    "int_pbi_admin__report_access",
    "int_pbi_admin__semantic_model_access",
]


@asset(
    group_name="export",
    kinds={"duckdb", "azure"},
    op_tags={"dagster/concurrency_key": "duckdb"},
    tags={"daily_pbi_intermediate": ""},
    deps=[
        AssetKey(["intermediate", "int_pbi_admin__reports"]),
        AssetKey(["intermediate", "int_pbi_admin__semantic_model_datasources"]),
        AssetKey(["intermediate", "int_pbi_admin__report_access"]),
        AssetKey(["intermediate", "int_pbi_admin__semantic_model_access"]),
        "azure_container_pbi_intermediate",
    ],
    description=(
        "Exports the four int_pbi_admin__* intermediate views from DuckDB as "
        "Parquet files to Azure Blob Storage. Runs after the daily dbt "
        "intermediate models have been materialised."
    ),
)
def pbi_intermediate_export(context: AssetExecutionContext) -> None:
    account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
    container = os.environ["PBI_INTERMEDIATE_CONTAINER"]
    blob_prefix = os.environ.get("PBI_INTERMEDIATE_EXPORT_PATH", "pbi_admin/")

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
        for view in _PBI_INTERMEDIATE_VIEWS:
            arrow_table: pa.Table = conn.execute(
                f"SELECT * FROM main_intermediate.{view};"
            ).fetch_arrow_table()

            buffer = io.BytesIO()
            pq.write_table(arrow_table, buffer, compression="snappy")
            buffer.seek(0)

            blob_name = f"{blob_prefix}{view}.parquet"
            blob_service.get_blob_client(
                container=container, blob=blob_name
            ).upload_blob(buffer, overwrite=True)

            context.log.info(
                f"Exported {len(arrow_table):,} rows → {blob_name}"
            )
