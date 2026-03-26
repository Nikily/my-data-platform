"""
8x8 Call Detail Records (CDR) ingestion asset.

Incrementally loads call records from the 8x8 Work Analytics API into DuckDB.

PBX LIST:
  The list of PBX IDs to ingest is read from docs/8x8/pbx.csv, which is the
  single source of truth. To add or remove a PBX, edit that file — no code
  or .env changes needed.

  One API call is made per PBX per run. All records land in a single DuckDB
  table (raw_eight_x_eight.call_detail_records). The pbx_id field in every
  record identifies which PBX it came from.

INCREMENTAL STRATEGY:
  - Initial load starts from 2026-03-01 00:00:00 CET (Europe/Paris).
  - Each PBX has its own independent dlt pipeline (pipeline_name includes the
    pbx_id), so each PBX tracks its own watermark separately. A failure on
    one PBX does not affect the others.
  - dlt tracks the maximum startTimeUTC (epoch ms) per PBX. On each run it
    queries from that watermark forward to now.
  - callId is used as the primary key — dlt performs a MERGE into DuckDB so
    duplicate records from overlapping windows are safely deduplicated.

PAGINATION:
  - The API uses a scrollId cursor. When the response meta includes a scrollId
    it is passed back as the sole query parameter on the next request.
  - pageSize is set to the API maximum (7000) to minimise round trips.

CREDENTIALS (set in .env):
  EIGHT_X_EIGHT_BASE_URL   Base URL of the 8x8 Analytics API
                           e.g. https://analytics.8x8.com
  EIGHT_X_EIGHT_API_KEY    API key sent as the `8x8-apikey` request header
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

# Initial load watermark: 2026-03-01 00:00:00 CET → epoch milliseconds.
_INITIAL_LOAD_UTC_MS: int = int(
    datetime(2026, 3, 1, 0, 0, 0, tzinfo=_CET).timestamp() * 1000
)

# The dbt seed is the single source of truth for the PBX list.
# To add or remove a PBX, edit dbt_project/seeds/8x8/pbx_country_mapping.csv.
_PBX_CSV = Path(__file__).parent.parent.parent.parent / "dbt_project" / "seeds" / "8x8" / "pbx_country_mapping.csv"

_ENDPOINT = "/api/analytics/report/external/v2/call-records"
_PAGE_SIZE = 7000       # API maximum
_TIMEZONE = "Europe/Paris"
_REQUEST_TIMEOUT = 60   # seconds


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_pbx_list() -> list[tuple[str, str]]:
    """
    Read the PBX list from dbt_project/seeds/8x8/pbx_country_mapping.csv.
    Returns a list of (pbx_id, country) tuples.
    """
    with open(_PBX_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [(row["pbx_id"].strip(), row["country"].strip()) for row in reader if row["pbx_id"].strip()]


def _headers() -> dict:
    return {"Authorization": f"Bearer {os.environ['EIGHT_X_EIGHT_API_KEY']}"}


def _epoch_ms_to_api_str(epoch_ms: int) -> str:
    """
    Convert epoch milliseconds to the 'YYYY-MM-DD HH:MM:SS' string format
    expected by the 8x8 API, expressed in the CET/CEST timezone.
    """
    dt = datetime.fromtimestamp(epoch_ms / 1000, tz=_CET)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _pipeline_name(pbx_id: str) -> str:
    """Produce a safe dlt pipeline name for a given PBX ID."""
    return "eight_x_eight_cdr_" + pbx_id.replace("-", "_").replace(" ", "_")


# ── dlt resource ──────────────────────────────────────────────────────────────

@dlt.resource(
    name="call_detail_records",
    write_disposition="merge",
    primary_key="callId",
)
def call_detail_records_resource(
    pbx_id: str,
    start_time_utc: dlt.sources.incremental[int] = dlt.sources.incremental(
        "startTimeUTC",
        initial_value=_INITIAL_LOAD_UTC_MS,
    ),
) -> Iterator[list]:
    """
    Fetches CDR records for a single PBX from the 8x8 Work Analytics API.

    The `start_time_utc` incremental parameter is automatically managed by dlt
    and is tracked independently per pipeline (i.e. per PBX):
      - First run:       uses _INITIAL_LOAD_UTC_MS (2026-03-01 00:00:00 CET)
      - Subsequent runs: uses the maximum startTimeUTC seen in the previous load
                         for this specific PBX
    """
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")

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


# ── Dagster asset ─────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description=(
        "Incrementally loads 8x8 Work CDR data into DuckDB for each PBX defined "
        "in docs/8x8/pbx.csv. Each PBX has an independent watermark starting from "
        "2026-03-01 CET. All records land in raw_eight_x_eight.call_detail_records."
    ),
)
def eight_x_eight_cdr_raw(context: AssetExecutionContext) -> None:
    pbx_list = _load_pbx_list()
    context.log.info(f"Loaded {len(pbx_list)} PBX(es) from pbx.csv: {[p for p, _ in pbx_list]}")

    for pbx_id, country in pbx_list:
        context.log.info(f"Starting ingestion for PBX '{pbx_id}' ({country})")

        pipeline = dlt.pipeline(
            # Unique pipeline name per PBX ensures independent incremental state.
            pipeline_name=_pipeline_name(pbx_id),
            destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
            # All PBXs write to the same schema and table so dbt works against
            # a single unified source.
            dataset_name="raw_eight_x_eight",
        )
        load_info = pipeline.run(call_detail_records_resource(pbx_id=pbx_id))
        context.log.info(f"PBX '{pbx_id}' done: {load_info}")
