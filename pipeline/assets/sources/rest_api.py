"""
REST API ingestion asset.

Uses dlt with incremental loading (cursor-based) to pull data from a REST API
and write it into the DuckDB raw layer.

HOW TO CUSTOMISE:
  1. Set REST_API_BASE_URL and REST_API_TOKEN in your .env file.
  2. Add one @dlt.resource function per endpoint you want to ingest.
  3. Adjust `primary_key` and `cursor_field` to match the API response shape.
  4. If the API returns paginated results, add a pagination loop inside the
     resource function.
"""

import os

import dlt
import requests
from dagster import AssetExecutionContext, asset


def _get_headers() -> dict:
    return {"Authorization": f"Bearer {os.environ['REST_API_TOKEN']}"}


@dlt.resource(
    name="orders",
    write_disposition="merge",
    primary_key="id",
)
def orders_resource(
    updated_at: dlt.sources.incremental[str] = dlt.sources.incremental(
        "updated_at",
        initial_value="2020-01-01T00:00:00Z",
    ),
):
    """
    Example resource: fetches orders updated since the last run.

    Replace this with your actual endpoint and response structure.
    The `updated_at` incremental parameter is automatically tracked by dlt —
    on subsequent runs it will only fetch records newer than the last loaded value.
    """
    base_url = os.environ["REST_API_BASE_URL"]
    params = {"updated_since": updated_at.last_value, "limit": 500}

    while True:
        response = requests.get(
            f"{base_url}/orders",
            headers=_get_headers(),
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        records = data.get("results", data) if isinstance(data, dict) else data
        if not records:
            break

        yield records

        # Handle pagination — adjust to match your API's pagination scheme.
        next_page = data.get("next") if isinstance(data, dict) else None
        if not next_page:
            break
        params["page"] = data.get("page", 1) + 1


@dlt.source(name="rest_api")
def rest_api_source():
    """Groups all REST API resources into a single dlt source."""
    return orders_resource()


@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    op_tags={"dagster/concurrency_key": "duckdb"},
    description="Incrementally loads data from the REST API into DuckDB (raw layer).",
)
def rest_api_raw(context: AssetExecutionContext) -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_rest_api",
    )
    load_info = pipeline.run(rest_api_source())
    context.log.info(str(load_info))
