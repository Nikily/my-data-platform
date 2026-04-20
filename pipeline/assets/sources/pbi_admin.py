"""
Power BI Admin REST API ingestion asset.

Loads a full snapshot of all Power BI Admin API endpoints into DuckDB
under the `raw_pbi_admin` schema. All tables are replaced on every run
(no incremental strategy — these are tenant-wide admin snapshots).

ENDPOINTS LOADED:
  apps                  GET /admin/apps
  capacities            GET /admin/capacities
  refreshables          GET /admin/capacities/refreshables
  groups                GET /admin/groups  (workspaces)
  dashboards            GET /admin/dashboards
  reports               GET /admin/reports
  datasets              GET /admin/datasets
  widely_shared_artifacts  GET /admin/widelySharedArtifacts/linksSharedToWholeOrganization
  unused_artifacts      GET /admin/groups/{groupId}/unused  (one call per workspace)

WORKSPACE SCANNER (separate asset):
  scanner_workspaces    POST /admin/workspaces/getInfo  (trigger)
                        GET  /admin/workspaces/scanStatus/{scanId}  (poll)
                        GET  /admin/workspaces/scanResult/{scanId}  (fetch)
  Processes Active non-personal workspaces in batches of 100.
  Returns workspace metadata plus per-artifact user access details for
  reports, datasets, dashboards, and dataflows.

AUTHENTICATION:
  Service principal via MSAL client credentials flow.
  Reads AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET from the environment.

CREDENTIALS (set in .env):
  PBI_REST_API_BASE_URL   e.g. https://api.powerbi.com/v1.0/myorg/admin
  AZURE_TENANT_ID
  AZURE_CLIENT_ID
  AZURE_CLIENT_SECRET
"""

import os
import time
from typing import Iterator

import dlt
import duckdb
import requests
from dagster import AssetExecutionContext, RetryPolicy, asset
from pipeline.utils.pbi import fetch_pbi_token

_PAGE_SIZE = 500        # used for $top/$skip endpoints
_GROUPS_PAGE_SIZE = 5000  # groups endpoint supports up to 5000
_TIMEOUT = 60
_UNUSED_CALL_DELAY = 0.5   # seconds between per-workspace unused-artifacts calls
_RATE_LIMIT_BACKOFF = 65   # seconds to wait on a 429 before retrying once
_SCANNER_BATCH_SIZE = 100  # max workspaces per PostWorkspaceInfo call
_SCANNER_POLL_INTERVAL = 10  # seconds between scanStatus polls
_SCANNER_MAX_POLLS = 60    # give up after 10 minutes per batch


# ── Helpers ────────────────────────────────────────────────────────────────────

def _base_url() -> str:
    return os.environ["PBI_REST_API_BASE_URL"].rstrip("/")


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _get(token: str, path: str, params: dict | None = None) -> dict:
    """GET with one automatic retry on 429 (rate limit)."""
    response = requests.get(
        f"{_base_url()}{path}",
        headers=_headers(token),
        params=params,
        timeout=_TIMEOUT,
    )
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", _RATE_LIMIT_BACKOFF))
        time.sleep(retry_after)
        response = requests.get(
            f"{_base_url()}{path}",
            headers=_headers(token),
            params=params,
            timeout=_TIMEOUT,
        )
    response.raise_for_status()
    return response.json()


def _post(token: str, path: str, params: dict | None = None, json_body: dict | None = None) -> dict:
    """POST with one automatic retry on 429 (rate limit)."""
    headers = {**_headers(token), "Content-Type": "application/json"}
    response = requests.post(
        f"{_base_url()}{path}",
        headers=headers,
        params=params,
        json=json_body,
        timeout=_TIMEOUT,
    )
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", _RATE_LIMIT_BACKOFF))
        time.sleep(retry_after)
        response = requests.post(
            f"{_base_url()}{path}",
            headers=headers,
            params=params,
            json=json_body,
            timeout=_TIMEOUT,
        )
    response.raise_for_status()
    return response.json()


def _wait_for_scan(token: str, scan_id: str) -> None:
    """Poll scanStatus until Succeeded, raise on failure or timeout."""
    for _ in range(_SCANNER_MAX_POLLS):
        status_data = _get(token, f"/workspaces/scanStatus/{scan_id}")
        status = status_data.get("status", "")
        if status == "Succeeded":
            return
        if status in ("Failed", "Cancelled"):
            raise RuntimeError(f"Scan {scan_id} ended with status: {status}")
        time.sleep(_SCANNER_POLL_INTERVAL)
    raise TimeoutError(
        f"Scan {scan_id} did not complete within "
        f"{_SCANNER_MAX_POLLS * _SCANNER_POLL_INTERVAL} seconds"
    )


# ── dlt resources ──────────────────────────────────────────────────────────────

@dlt.resource(name="apps", write_disposition="replace")
def apps_resource(token: str) -> Iterator[list]:
    """GET /apps — all installed apps in the tenant."""
    skip = 0
    while True:
        payload = _get(token, "/apps", {"$top": _PAGE_SIZE, "$skip": skip})
        records = payload.get("value", [])
        if not records:
            break
        yield records
        if len(records) < _PAGE_SIZE:
            break
        skip += _PAGE_SIZE


@dlt.resource(name="capacities", write_disposition="replace")
def capacities_resource(token: str) -> Iterator[list]:
    """GET /capacities — all Power BI capacities in the tenant."""
    payload = _get(token, "/capacities")
    records = payload.get("value", [])
    if records:
        yield records


@dlt.resource(name="refreshables", write_disposition="replace")
def refreshables_resource(token: str) -> Iterator[list]:
    """GET /capacities/refreshables — datasets with a refresh history or schedule."""
    skip = 0
    while True:
        payload = _get(token, "/capacities/refreshables", {"$top": _PAGE_SIZE, "$skip": skip, "$expand": "capacity,group"})
        records = payload.get("value", [])
        if not records:
            break
        yield records
        if len(records) < _PAGE_SIZE:
            break
        skip += _PAGE_SIZE


@dlt.resource(name="groups", write_disposition="replace")
def groups_resource(token: str) -> Iterator[list]:
    """GET /groups — all workspaces (groups) in the tenant."""
    skip = 0
    while True:
        payload = _get(token, "/groups", {"$top": _GROUPS_PAGE_SIZE, "$skip": skip})
        records = payload.get("value", [])
        if not records:
            break
        yield records
        if len(records) < _GROUPS_PAGE_SIZE:
            break
        skip += _GROUPS_PAGE_SIZE


@dlt.resource(name="dashboards", write_disposition="replace")
def dashboards_resource(token: str) -> Iterator[list]:
    """GET /dashboards — all dashboards in the tenant."""
    skip = 0
    while True:
        payload = _get(token, "/dashboards", {"$top": _PAGE_SIZE, "$skip": skip})
        records = payload.get("value", [])
        if not records:
            break
        yield records
        if len(records) < _PAGE_SIZE:
            break
        skip += _PAGE_SIZE


@dlt.resource(name="reports", write_disposition="replace")
def reports_resource(token: str) -> Iterator[list]:
    """GET /reports — all reports in the tenant."""
    skip = 0
    while True:
        payload = _get(token, "/reports", {"$top": _PAGE_SIZE, "$skip": skip})
        records = payload.get("value", [])
        if not records:
            break
        yield records
        if len(records) < _PAGE_SIZE:
            break
        skip += _PAGE_SIZE


@dlt.resource(name="datasets", write_disposition="replace")
def datasets_resource(token: str) -> Iterator[list]:
    """GET /datasets — all datasets (semantic models) in the tenant."""
    skip = 0
    while True:
        payload = _get(token, "/datasets", {"$top": _PAGE_SIZE, "$skip": skip})
        records = payload.get("value", [])
        if not records:
            break
        yield records
        if len(records) < _PAGE_SIZE:
            break
        skip += _PAGE_SIZE


@dlt.resource(name="widely_shared_artifacts", write_disposition="replace")
def widely_shared_artifacts_resource(token: str) -> Iterator[list]:
    """GET /widelySharedArtifacts/linksSharedToWholeOrganization — reports shared org-wide."""
    path = "/widelySharedArtifacts/linksSharedToWholeOrganization"
    params: dict = {}
    while True:
        payload = _get(token, path, params or None)
        records = payload.get("artifactAccessEntities", [])
        if records:
            yield records
        continuation_token = payload.get("continuationToken")
        if not continuation_token:
            break
        params = {"continuationToken": continuation_token}


def _run_scanner_batches(token: str, group_ids: list[str]) -> tuple[list, list]:
    """
    Run all scanner batches and return (all_workspaces, all_datasource_instances).
    Collects both top-level arrays from the scan result so a single API sweep
    populates both the workspace tree and the datasource lookup table.
    """
    all_workspaces: list = []
    all_datasource_instances: list = []
    scan_params = {
        "lineage": "true",
        "datasourceDetails": "true",
        "getArtifactUsers": "true",
    }
    for i in range(0, len(group_ids), _SCANNER_BATCH_SIZE):
        batch = group_ids[i : i + _SCANNER_BATCH_SIZE]
        trigger = _post(
            token,
            "/workspaces/getInfo",
            params=scan_params,
            json_body={"workspaces": batch},
        )
        scan_id = trigger["id"]
        _wait_for_scan(token, scan_id)
        result = _get(token, f"/workspaces/scanResult/{scan_id}")
        all_workspaces.extend(result.get("workspaces", []))
        all_datasource_instances.extend(result.get("datasourceInstances", []))
    return all_workspaces, all_datasource_instances


@dlt.resource(name="scanner_workspaces", write_disposition="replace")
def scanner_workspaces_resource(records: list) -> Iterator[list]:
    """Workspace tree from the scanner API, pre-collected by _run_scanner_batches."""
    if records:
        yield records


@dlt.resource(name="scanner_datasource_instances", write_disposition="replace")
def scanner_datasource_instances_resource(records: list) -> Iterator[list]:
    """
    Top-level datasource instances from the scanner API result.
    Contains connection details (type, server, database, path, url) for every
    datasource referenced by datasets in the scan. Linked to datasets via
    scanner_workspaces__datasets__datasource_usages.datasource_instance_id.
    """
    if records:
        yield records


@dlt.resource(name="unused_artifacts", write_disposition="replace")
def unused_artifacts_resource(token: str, group_ids: list[str]) -> Iterator[list]:
    """
    GET /groups/{groupId}/unused for each workspace.
    Only called for Active, non-personal workspaces to stay within the
    200 req/hr rate limit. Yields records enriched with group_id.
    """
    for group_id in group_ids:
        time.sleep(_UNUSED_CALL_DELAY)
        params: dict = {}
        while True:
            try:
                payload = _get(token, f"/groups/{group_id}/unused", params or None)
            except requests.exceptions.HTTPError as exc:
                # Some workspace types return 4xx — skip them cleanly
                if exc.response is not None and exc.response.status_code in (400, 403, 404):
                    break
                raise
            records = payload.get("unusedArtifactEntities", [])
            if records:
                enriched = [{**r, "group_id": group_id} for r in records]
                yield enriched
            continuation_token = payload.get("continuationToken")
            if not continuation_token:
                break
            params = {"continuationToken": continuation_token}


# ── Dagster assets ─────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description=(
        "Full snapshot of Power BI Admin REST API endpoints loaded into DuckDB. "
        "Covers apps, capacities, refreshables, groups (workspaces), dashboards, "
        "reports, datasets, and widely-shared artifacts."
    ),
)
def pbi_admin_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Power BI Bearer token via MSAL...")
    token = fetch_pbi_token()
    context.log.info("Token obtained.")

    pipeline = dlt.pipeline(
        pipeline_name="pbi_admin",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_pbi_admin",
    )

    load_info = pipeline.run(
        [
            apps_resource(token=token),
            capacities_resource(token=token),
            refreshables_resource(token=token),
            groups_resource(token=token),
            dashboards_resource(token=token),
            reports_resource(token=token),
            datasets_resource(token=token),
            widely_shared_artifacts_resource(token=token),
        ]
    )
    context.log.info(f"Load complete: {load_info}")


@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    deps=["pbi_admin_raw"],
    description=(
        "Sweeps all Active, non-personal workspaces for artifacts unused in 30+ days. "
        "Runs separately from pbi_admin_raw because the /groups/{id}/unused endpoint "
        "is limited to 200 req/hr — with hundreds of workspaces this can take a long time. "
        "Schedule this weekly rather than daily."
    ),
)
def pbi_admin_unused_artifacts_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Power BI Bearer token via MSAL...")
    token = fetch_pbi_token()
    context.log.info("Token obtained.")

    # Fetch only Active, non-personal workspaces to minimise API calls
    context.log.info("Fetching active workspaces...")
    group_ids: list[str] = []
    skip = 0
    _PERSONAL_TYPES = {"PersonalGroup", "Personal"}
    while True:
        payload = _get(token, "/groups", {"$top": _GROUPS_PAGE_SIZE, "$skip": skip})
        batch = payload.get("value", [])
        if not batch:
            break
        group_ids.extend(
            g["id"] for g in batch
            if g.get("state") == "Active" and g.get("type") not in _PERSONAL_TYPES
        )
        if len(batch) < _GROUPS_PAGE_SIZE:
            break
        skip += _GROUPS_PAGE_SIZE

    context.log.info(
        f"Found {len(group_ids)} active non-personal workspaces — "
        f"estimated time at 0.5 s/call: ~{len(group_ids) // 2} seconds."
    )

    pipeline = dlt.pipeline(
        pipeline_name="pbi_admin_unused",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_pbi_admin",
    )

    load_info = pipeline.run(
        unused_artifacts_resource(token=token, group_ids=group_ids)
    )
    context.log.info(f"Load complete: {load_info}")


@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    deps=["pbi_admin_raw"],
    description=(
        "Workspace Scanner API snapshot: workspace metadata plus per-artifact "
        "user access details (reports, datasets, dashboards, dataflows). "
        "Runs after pbi_admin_raw to avoid DuckDB write conflicts. "
        "Processes Active non-personal workspaces in batches of 100. "
        "Loads into raw_pbi_admin schema as scanner_workspaces and child tables."
    ),
)
def pbi_admin_scanner_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Power BI Bearer token via MSAL...")
    token = fetch_pbi_token()
    context.log.info("Token obtained.")

    # Fetch Active non-personal workspaces to scan
    context.log.info("Fetching active workspaces for scanner...")
    group_ids: list[str] = []
    skip = 0
    _PERSONAL_TYPES = {"PersonalGroup", "Personal"}
    while True:
        payload = _get(token, "/groups", {"$top": _GROUPS_PAGE_SIZE, "$skip": skip})
        batch = payload.get("value", [])
        if not batch:
            break
        group_ids.extend(
            g["id"] for g in batch
            if g.get("state") == "Active" and g.get("type") not in _PERSONAL_TYPES
        )
        if len(batch) < _GROUPS_PAGE_SIZE:
            break
        skip += _GROUPS_PAGE_SIZE

    n_batches = (len(group_ids) + _SCANNER_BATCH_SIZE - 1) // _SCANNER_BATCH_SIZE
    context.log.info(
        f"Found {len(group_ids)} active non-personal workspaces — "
        f"{n_batches} scan batches of up to {_SCANNER_BATCH_SIZE}."
    )

    all_workspaces, all_datasource_instances = _run_scanner_batches(token, group_ids)
    context.log.info(
        f"Scan complete — {len(all_workspaces)} workspaces, "
        f"{len(all_datasource_instances)} datasource instances collected."
    )

    pipeline = dlt.pipeline(
        pipeline_name="pbi_admin_scanner",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_pbi_admin",
    )

    load_info = pipeline.run([
        scanner_workspaces_resource(records=all_workspaces),
        scanner_datasource_instances_resource(records=all_datasource_instances),
    ])
    context.log.info(f"Load complete: {load_info}")


@dlt.resource(name="dataset_refreshes", write_disposition="append")
def dataset_refreshes_resource(token: str, dataset_ids: list[str]) -> Iterator[list]:
    """
    GET /admin/datasets/{datasetId}/refreshes?$top=5 for each dataset.
    Yields the last 5 refresh attempts per dataset, enriched with dataset_id.
    Skips datasets that return 4xx (e.g. personal workspaces, inaccessible datasets).
    write_disposition=append — each hourly run adds new rows; history is preserved.
    """
    for dataset_id in dataset_ids:
        try:
            payload = _get(
                token, f"/datasets/{dataset_id}/refreshes", {"$top": 5}
            )
        except requests.exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code in (400, 403, 404):
                continue
            raise
        records = payload.get("value", [])
        if records:
            yield [{**r, "dataset_id": dataset_id} for r in records]


@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    retry_policy=RetryPolicy(max_retries=1, delay=300),
    description=(
        "Hourly snapshot of the last 5 refresh attempts per refreshable dataset. "
        "Calls GET /admin/datasets/{id}/refreshes for each dataset where "
        "is_refreshable=true. Appends to dataset_refreshes in raw_pbi_admin — "
        "history is preserved across runs. "
        "RetryPolicy: 1 retry after 5 minutes to ride out any DuckDB write lock "
        "from the daily pipeline."
    ),
)
def pbi_admin_refreshes_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Power BI Bearer token via MSAL...")
    token = fetch_pbi_token()
    context.log.info("Token obtained.")

    # Read refreshable dataset IDs from DuckDB (written by pbi_admin_raw daily)
    context.log.info("Reading refreshable dataset IDs from DuckDB...")
    conn = duckdb.connect(os.environ["DUCKDB_PATH"], read_only=True)
    try:
        rows = conn.execute(
            "SELECT id FROM raw_pbi_admin.datasets WHERE is_refreshable = true"
        ).fetchall()
    finally:
        conn.close()

    dataset_ids = [row[0] for row in rows if row[0]]
    context.log.info(f"Found {len(dataset_ids)} refreshable datasets.")

    pipeline = dlt.pipeline(
        pipeline_name="pbi_admin_refreshes",
        destination=dlt.destinations.duckdb(credentials=os.environ["DUCKDB_PATH"]),
        dataset_name="raw_pbi_admin",
    )

    load_info = pipeline.run(
        dataset_refreshes_resource(token=token, dataset_ids=dataset_ids)
    )
    context.log.info(f"Load complete: {load_info}")
