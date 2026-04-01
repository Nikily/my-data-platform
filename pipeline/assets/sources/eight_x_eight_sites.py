"""
8x8 PBX Sites ingestion asset.

Fetches the list of sites for each PBX (from the seed CSV) using the
8x8 Analytics API. Uses the same Bearer token as the CDR asset.

Endpoint: GET /analytics/work/v2/pbxes/{pbxId}/sites
Auth:     Same as CDR — Analytics OAuth token + 8x8-apikey header

CREDENTIALS (set in .env):
  EIGHT_X_EIGHT_BASE_URL   Base URL, e.g. https://api.8x8.com
  EIGHT_X_EIGHT_API_KEY    API key sent as the `8x8-apikey` header
  EIGHT_X_EIGHT_USERNAME   Username for token exchange
  EIGHT_X_EIGHT_PASSWORD   Password for token exchange
"""

import csv
import os
from pathlib import Path
from typing import Iterator

import dlt
import requests
from dagster import AssetExecutionContext, asset
from pipeline.utils.eight_x_eight import fetch_token

_SITES_PATH = "/analytics/work/v2/pbxes/{pbx_id}/sites"
_PAGE_SIZE  = 100
_TIMEOUT    = 60

_PBX_CSV = (
    Path(__file__).parent.parent.parent.parent
    / "dbt_project" / "seeds" / "8x8" / "pbx_country_mapping.csv"
)


def _load_pbx_ids() -> list[str]:
    with open(_PBX_CSV, newline="", encoding="utf-8") as f:
        return [row["pbx_id"].strip() for row in csv.DictReader(f) if row["pbx_id"].strip()]


# ── dlt resource ──────────────────────────────────────────────────────────────

@dlt.resource(
    name="pbx_sites",
    write_disposition="replace",
    primary_key="id",
)
def pbx_sites_resource(token: str) -> Iterator[list]:
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")
    headers = {
        "Authorization": f"Bearer {token}",
        "8x8-apikey": os.environ["EIGHT_X_EIGHT_API_KEY"],
    }

    for pbx_id in _load_pbx_ids():
        page = 0
        while True:
            response = requests.get(
                f"{base_url}{_SITES_PATH.format(pbx_id=pbx_id)}",
                headers=headers,
                params={"page": page, "size": _PAGE_SIZE},
                timeout=_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()

            sites: list = payload.get("_embedded", {}).get("siteList", [])
            if not sites:
                break

            yield sites

            page_meta = payload.get("page", {})
            total_pages = page_meta.get("totalPages", 1)
            page += 1
            if page >= total_pages:
                break


@dlt.source(name="eight_x_eight_analytics")
def eight_x_eight_sites_source(token: str) -> dlt.sources.DltSource:
    return pbx_sites_resource(token=token)


# ── Dagster asset ─────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description=(
        "Loads 8x8 site lists for all PBXs into DuckDB. "
        "Full replace on each run. PBX list is read from the seed CSV."
    ),
)
def eight_x_eight_sites_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Bearer token from 8x8 token endpoint...")
    token = fetch_token()
    context.log.info("Token obtained. Fetching sites for all PBXs...")

    pipeline = dlt.pipeline(
        pipeline_name="eight_x_eight_sites",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_eight_x_eight",
    )
    load_info = pipeline.run(eight_x_eight_sites_source(token=token))
    context.log.info(f"Sites load done: {load_info}")
