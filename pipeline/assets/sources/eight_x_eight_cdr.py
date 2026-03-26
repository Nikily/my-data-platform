"""
8x8 Call Detail Records (CDR) ingestion asset.

Incrementally loads call records from the 8x8 Work Analytics API into DuckDB.

AUTHENTICATION:
  The API uses a two-step OAuth2 flow:
    1. POST /v1/oauth/token with the 8x8-apikey header and username/password
       in the request body to obtain a short-lived Bearer token (30 min TTL).
    2. Use Authorization: Bearer <token> on all subsequent CDR API calls.
  A fresh token is fetched once at the start of each Dagster asset run and
  reused for all PBX calls within that run.

PBX LIST:
  Read from dbt_project/seeds/8x8/pbx_country_mapping.csv — the single source
  of truth. To add or remove a PBX, edit only that file.
  One API call is made per PBX per run. All records land in a single DuckDB
  table (raw_eight_x_eight.call_detail_records).

INCREMENTAL STRATEGY:
  - Initial load starts from 2026-03-01 00:00:00 CET (Europe/Paris).
  - Each PBX has its own independent dlt pipeline (pipeline_name includes the
    pbx_id), so each PBX tracks its own watermark separately.
  - callId is used as the primary key — dlt performs a MERGE into DuckDB so
    duplicate records from overlapping windows are safely deduplicated.

PAGINATION:
  - The API uses a scrollId cursor. pageSize is set to the API maximum (7000).

CREDENTIALS (set in .env):
  EIGHT_X_EIGHT_BASE_URL   Base URL, e.g. https://api.8x8.com
  EIGHT_X_EIGHT_API_KEY    API key sent as the `8x8-apikey` header to the
                           token endpoint
  EIGHT_X_EIGHT_USERNAME   Username for token exchange
  EIGHT_X_EIGHT_PASSWORD   Password for token exchange
"""

import csv
import os
import zoneinfo
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import dlt
import requests
from dagster import AssetExecutionContext, asset

# ── Constants ─────────────────────────────────────────────────────────────────

_CET = zoneinfo.ZoneInfo("Europe/Paris")

_INITIAL_LOAD_UTC_MS: int = int(
    datetime(2026, 3, 1, 0, 0, 0, tzinfo=_CET).timestamp() * 1000
)

_PBX_CSV = (
    Path(__file__).parent.parent.parent.parent
    / "dbt_project" / "seeds" / "8x8" / "pbx_country_mapping.csv"
)

_TOKEN_PATH = "/v1/oauth/token"
_CDR_PATH   = "/api/analytics/report/external/v2/call-records"
_PAGE_SIZE  = 7000
_TIMEZONE   = "Europe/Paris"
_TIMEOUT    = 60


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_pbx_list() -> list[tuple[str, str]]:
    with open(_PBX_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            (row["pbx_id"].strip(), row["country"].strip())
            for row in reader if row["pbx_id"].strip()
        ]


def _fetch_token() -> str:
    """
    Exchange username + password for a Bearer token via POST /v1/oauth/token.
    The 8x8-apikey header identifies the application; the body carries the
    user credentials. Returns the access_token string (valid for 30 minutes).
    """
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")
    response = requests.post(
        f"{base_url}{_TOKEN_PATH}",
        headers={"8x8-apikey": os.environ["EIGHT_X_EIGHT_API_KEY"]},
        data={
            "username": os.environ["EIGHT_X_EIGHT_USERNAME"],
            "password": os.environ["EIGHT_X_EIGHT_PASSWORD"],
        },
        timeout=_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def _epoch_ms_to_api_str(epoch_ms: int) -> str:
    dt = datetime.fromtimestamp(epoch_ms / 1000, tz=_CET)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _pipeline_name(pbx_id: str) -> str:
    return "eight_x_eight_cdr_" + pbx_id.replace("-", "_").replace(" ", "_")


# ── dlt resource ──────────────────────────────────────────────────────────────

@dlt.resource(
    name="call_detail_records",
    write_disposition="merge",
    primary_key="callId",
)
def call_detail_records_resource(
    pbx_id: str,
    token: str,
    start_time_utc: dlt.sources.incremental[int] = dlt.sources.incremental(
        "startTimeUTC",
        initial_value=_INITIAL_LOAD_UTC_MS,
    ),
) -> Iterator[list]:
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")
    headers  = {"Authorization": f"Bearer {token}"}

    window_start = _epoch_ms_to_api_str(start_time_utc.last_value)
    window_end   = _epoch_ms_to_api_str(int(datetime.now(timezone.utc).timestamp() * 1000))

    params: dict = {
        "pbxId":     pbx_id,
        "startTime": window_start,
        "endTime":   window_end,
        "timeZone":  _TIMEZONE,
        "pageSize":  _PAGE_SIZE,
    }

    while True:
        response = requests.get(
            f"{base_url}{_CDR_PATH}",
            headers=headers,
            params=params,
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()

        records: list = payload.get("data", [])
        if not records:
            break

        yield records

        scroll_id: str | None = payload.get("meta", {}).get("scrollId")
        if not scroll_id:
            break

        params = {"scrollId": scroll_id}


@dlt.source(name="eight_x_eight")
def eight_x_eight_source(pbx_id: str, token: str) -> dlt.sources.DltSource:
    return call_detail_records_resource(pbx_id=pbx_id, token=token)


# ── Dagster asset ─────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description=(
        "Incrementally loads 8x8 Work CDR data into DuckDB for each PBX defined "
        "in dbt_project/seeds/8x8/pbx_country_mapping.csv. Fetches a Bearer token "
        "once per run via OAuth2, then queries each PBX independently."
    ),
)
def eight_x_eight_cdr_raw(context: AssetExecutionContext) -> None:
    pbx_list = _load_pbx_list()
    context.log.info(f"Loaded {len(pbx_list)} PBX(es): {[p for p, _ in pbx_list]}")

    context.log.info("Fetching Bearer token from 8x8 token endpoint...")
    token = _fetch_token()
    context.log.info("Token obtained successfully.")

    for pbx_id, country in pbx_list:
        context.log.info(f"Ingesting PBX '{pbx_id}' ({country})")
        pipeline = dlt.pipeline(
            pipeline_name=_pipeline_name(pbx_id),
            destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
            dataset_name="raw_eight_x_eight",
        )
        load_info = pipeline.run(eight_x_eight_source(pbx_id=pbx_id, token=token))
        context.log.info(f"PBX '{pbx_id}' done: {load_info}")
