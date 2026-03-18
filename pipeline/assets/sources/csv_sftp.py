"""
SFTP CSV ingestion asset.

Uses dlt's filesystem source with the sshfs backend to read CSV files from an
SFTP server and write them into the DuckDB raw layer.

HOW TO CUSTOMISE:
  1. Set SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD and SFTP_PATH
     in your .env file.
  2. Adjust the glob pattern to match your file naming convention.
  3. dlt tracks which files have already been loaded, so only new files are
     processed on subsequent runs.

DEPENDENCY:
  The `sshfs` Python package must be installed (it is in pyproject.toml).
  It provides the fsspec SSH/SFTP backend used by dlt's filesystem source.
"""

import os

import dlt
from dlt.sources.filesystem import filesystem, read_csv
from dagster import AssetExecutionContext, asset


@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description="Loads CSV files from an SFTP server into DuckDB (raw layer).",
)
def csv_sftp_raw(context: AssetExecutionContext) -> None:
    host = os.environ["SFTP_HOST"]
    port = os.environ.get("SFTP_PORT", "22")
    username = os.environ["SFTP_USERNAME"]
    password = os.environ["SFTP_PASSWORD"]
    path = os.environ.get("SFTP_PATH", "/")

    # dlt uses fsspec under the hood. The SFTP URL format is:
    #   sftp://username:password@host:port/path
    sftp_url = f"sftp://{username}:{password}@{host}:{port}{path}"

    source = filesystem(
        bucket_url=sftp_url,
        file_glob="**/*.csv",
    ) | read_csv()

    pipeline = dlt.pipeline(
        pipeline_name="csv_sftp",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_csv_sftp",
    )
    load_info = pipeline.run(source)
    context.log.info(str(load_info))
