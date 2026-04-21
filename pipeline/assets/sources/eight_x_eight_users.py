"""
8x8 Users ingestion asset.

Loads the full list of users from the 8x8 Admin Provisioning API into DuckDB.
Runs a full replace on each execution — user lists are small enough that
incremental loading adds no meaningful benefit.

The nested `serviceInfo.extensions` array is flattened by dlt into a child
table (users__service_info__extensions) which is joined in the staging model
to produce one row per user-extension combination.

AUTHENTICATION:
  Same Bearer token as the CDR asset (Analytics OAuth endpoint).

CREDENTIALS (set in .env):
  EIGHT_X_EIGHT_BASE_URL   Base URL, e.g. https://api.8x8.com
  EIGHT_X_EIGHT_API_KEY    API key sent as the `8x8-apikey` header
  EIGHT_X_EIGHT_USERNAME   Username for token exchange
  EIGHT_X_EIGHT_PASSWORD   Password for token exchange
"""

import os
from typing import Iterator

import dlt
import requests
from dagster import AssetExecutionContext, asset
from pipeline.utils.eight_x_eight import fetch_token

_USERS_PATH = "/admin-provisioning/users"
_PAGE_SIZE  = 100
_TIMEOUT    = 60


# ── dlt resource ──────────────────────────────────────────────────────────────

@dlt.resource(
    name="users",
    write_disposition="replace",
    primary_key="basic_info__user_id",
)
def users_resource(token: str) -> Iterator[list]:
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")
    headers = {
        "Authorization": f"Bearer {token}",
        "8x8-apikey": os.environ["EIGHT_X_EIGHT_API_KEY"],
    }

    params: dict = {"pageSize": _PAGE_SIZE}

    while True:
        response = requests.get(
            f"{base_url}{_USERS_PATH}",
            headers=headers,
            params=params,
            timeout=_TIMEOUT,
        )

        # Expired scroll cursor — stop cleanly
        if response.status_code == 400 and "scrollId" in params:
            break

        response.raise_for_status()
        payload = response.json()

        records: list = payload.get("data", [])
        if not records:
            break

        yield records

        pagination = payload.get("pagination", {})
        next_scroll_id: str | None = pagination.get("nextScrollId")
        if not next_scroll_id or not pagination.get("hasMore", False):
            break

        params = {"scrollId": next_scroll_id}


@dlt.source(name="eight_x_eight_admin")
def eight_x_eight_admin_source(token: str) -> dlt.sources.DltSource:
    return users_resource(token=token)


# ── Dagster asset ─────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    op_tags={"dagster/concurrency_key": "duckdb"},
    description=(
        "Loads the full 8x8 user list from the Admin Provisioning API into DuckDB. "
        "Full replace on each run. Extensions are stored in a child table by dlt."
    ),
)
def eight_x_eight_users_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Bearer token from 8x8 token endpoint...")
    token = fetch_token()
    context.log.info("Token obtained successfully.")

    pipeline = dlt.pipeline(
        pipeline_name="eight_x_eight_users",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_eight_x_eight",
    )
    load_info = pipeline.run(eight_x_eight_admin_source(token=token))
    context.log.info(f"Users load done: {load_info}")
