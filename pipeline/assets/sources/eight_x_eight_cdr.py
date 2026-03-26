"""
8x8 Call Detail Records (CDR) ingestion asset.

Incrementally loads call records from the 8x8 Work Analytics API into DuckDB.

INCREMENTAL STRATEGY:
  - Initial load starts from 2026-03-01 00:00:00 CET (Europe/Paris).
  - dlt tracks the maximum `startTimeUTC` (epoch ms) seen across all loaded
    records. On each subsequent run it queries from that watermark forward to
    now, so only new records are fetched.
  - `callId` is used as the primary key — dlt performs a MERGE into DuckDB
    so duplicate records from any overlapping windows are safely deduplicated.

PAGINATION:
  - The API uses a scrollId cursor. When the response meta includes a scrollId
    it is passed back as the sole query parameter on the next request.
  - pageSize is set to the API maximum (7000) to minimise round trips.

CREDENTIALS (set all of these in .env):
  EIGHT_X_EIGHT_BASE_URL   Base URL of the 8x8 Analytics API
                           e.g. https://analytics.8x8.com
  EIGHT_X_EIGHT_API_KEY    API key sent as the `8x8-apikey` request header
  EIGHT_X_EIGHT_PBX_ID     PBX ID to query, or `allpbxes` for all PBXs in
                           the account
"""

import os
import zoneinfo
from datetime import datetime, timezone
from typing import Iterator

import dlt
import requests
from dagster import AssetExecutionContext, asset

# ── Constants ─────────────────────────────────────────────────────────────────

_CET = zoneinfo.ZoneInfo("Europe/Paris")

# Initial load watermark: 2026-03-01 00:00:00 CET → epoch milliseconds.
_INITIAL_LOAD_UTC_MS: int = int(
    datetime(2026, 3, 1, 0, 0, 0, tzinfo=_CET).timestamp() * 1000
)

_ENDPOINT = "/api/analytics/report/external/v2/call-records"
_PAGE_SIZE = 7000       # API maximum
_TIMEZONE = "Europe/Paris"
_REQUEST_TIMEOUT = 60   # seconds


# ── Helpers ───────────────────────────────────────────────────────────────────

def _headers() -> dict:
    return {"8x8-apikey": os.environ["EIGHT_X_EIGHT_API_KEY"]}


def _epoch_ms_to_api_str(epoch_ms: int) -> str:
    """
    Convert epoch milliseconds to the 'YYYY-MM-DD HH:MM:SS' string format
    expected by the 8x8 API, expressed in the CET timezone.
    """
    dt = datetime.fromtimestamp(epoch_ms / 1000, tz=_CET)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# ── dlt resource ──────────────────────────────────────────────────────────────

@dlt.resource(
    name="call_detail_records",
    write_disposition="merge",
    primary_key="callId",
)
def call_detail_records_resource(
    start_time_utc: dlt.sources.incremental[int] = dlt.sources.incremental(
        "startTimeUTC",
        initial_value=_INITIAL_LOAD_UTC_MS,
    ),
) -> Iterator[list]:
    """
    Fetches CDR records from the 8x8 Work Analytics API with scroll-based
    pagination.

    The `start_time_utc` incremental parameter is automatically managed by dlt:
      - First run:      uses _INITIAL_LOAD_UTC_MS (2026-03-01 00:00:00 CET)
      - Subsequent runs: uses the maximum startTimeUTC seen in the previous load

    The API time window is:
      startTime = last watermark (CET string)
      endTime   = now (CET string)
    """
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")
    pbx_id = os.environ["EIGHT_X_EIGHT_PBX_ID"]

    window_start = _epoch_ms_to_api_str(start_time_utc.last_value)
    window_end = _epoch_ms_to_api_str(
        int(datetime.now(timezone.utc).timestamp() * 1000)
    )

    # First-page parameters — subsequent pages only need scrollId.
    params: dict = {
        "pbxId": pbx_id,
        "startTime": window_start,
        "endTime": window_end,
        "timeZone": _TIMEZONE,
        "pageSize": _PAGE_SIZE,
    }

    while True:
        response = requests.get(
            f"{base_url}{_ENDPOINT}",
            headers=_headers(),
            params=params,
            timeout=_REQUEST_TIMEOUT,
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

        # Only scrollId is needed for subsequent pages.
        params = {"scrollId": scroll_id}


@dlt.source(name="eight_x_eight")
def eight_x_eight_source() -> dlt.sources.DltSource:
    return call_detail_records_resource()


# ── Dagster asset ─────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description=(
        "Incrementally loads 8x8 Work Call Detail Records into DuckDB. "
        "Initial load from 2026-03-01 00:00:00 CET; subsequent runs fetch "
        "records since the last loaded startTimeUTC. Deduplicates on callId."
    ),
)
def eight_x_eight_cdr_raw(context: AssetExecutionContext) -> None:
    pipeline = dlt.pipeline(
        pipeline_name="eight_x_eight_cdr",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_eight_x_eight",
    )
    load_info = pipeline.run(eight_x_eight_source())
    context.log.info(str(load_info))
