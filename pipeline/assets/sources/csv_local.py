"""
Local CSV ingestion asset.

Uses dlt's filesystem source to read CSV files from a local directory and
write them into the DuckDB raw layer.

HOW TO CUSTOMISE:
  1. Set LOCAL_CSV_PATH in your .env file to the directory containing CSV files.
  2. Adjust the glob pattern to match your file naming convention.
  3. If files represent daily snapshots (e.g. orders_2024-01-15.csv), the
     file-modification-based incremental logic will only pick up new files.
"""

import os

import dlt
from dlt.sources.filesystem import filesystem, read_csv
from dagster import AssetExecutionContext, asset


@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    op_tags={"dagster/concurrency_key": "duckdb"},
    description="Loads CSV files from a local directory into DuckDB (raw layer).",
)
def csv_local_raw(context: AssetExecutionContext) -> None:
    local_path = os.environ.get("LOCAL_CSV_PATH", "/opt/my_data_platform/data/csv")

    # The filesystem source picks up all CSV files under the given path.
    # dlt tracks which files have already been loaded via its internal state,
    # so rerunning the pipeline only processes new or modified files.
    source = filesystem(
        bucket_url=local_path,
        file_glob="**/*.csv",
    ) | read_csv()

    pipeline = dlt.pipeline(
        pipeline_name="csv_local",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_csv_local",
    )
    load_info = pipeline.run(source)
    context.log.info(str(load_info))
