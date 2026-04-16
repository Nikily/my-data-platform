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
from typing import Iterator

import dlt
import requests
from dagster import AssetExecutionContext, asset
from pipeline.utils.pbi import fetch_pbi_token

_PAGE_SIZE = 500        # used for $top/$skip endpoints
_GROUPS_PAGE_SIZE = 5000  # groups endpoint supports up to 5000
_TIMEOUT = 60


# ── Helpers ────────────────────────────────────────────────────────────────────

def _base_url() -> str:
    return os.environ["PBI_REST_API_BASE_URL"].rstrip("/")


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _get(token: str, path: str, params: dict | None = None) -> dict:
    response = requests.get(
        f"{_base_url()}{path}",
        headers=_headers(token),
        params=params,
        timeout=_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


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
        payload = _get(token, "/capacities/refreshables", {"$top": _PAGE_SIZE, "$skip": skip})
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


@dlt.resource(name="unused_artifacts", write_disposition="replace")
def unused_artifacts_resource(token: str, group_ids: list[str]) -> Iterator[list]:
    """
    GET /groups/{groupId}/unused for each workspace.
    Yields records enriched with group_id so the workspace is identifiable.
    """
    for group_id in group_ids:
        params: dict = {}
        while True:
            try:
                payload = _get(token, f"/groups/{group_id}/unused", params or None)
            except requests.exceptions.HTTPError as exc:
                # Some workspace types (personal, read-only) return 4xx — skip them
                if exc.response is not None and exc.response.status_code in (400, 403, 404):
                    break
                raise
            records = payload.get("unusedArtifactEntities", [])
            if records:
                # Enrich with workspace ID for joinability
                enriched = [{**r, "group_id": group_id} for r in records]
                yield enriched
            continuation_token = payload.get("continuationToken")
            if not continuation_token:
                break
            params = {"continuationToken": continuation_token}


# ── Dagster asset ──────────────────────────────────────────────────────────────

@asset(
    group_name="raw_ingestion",
    kinds={"dlt", "duckdb"},
    description=(
        "Full snapshot of all Power BI Admin REST API endpoints loaded into DuckDB. "
        "Covers apps, capacities, refreshables, groups (workspaces), dashboards, "
        "reports, datasets, widely-shared artifacts, and unused artifacts per workspace."
    ),
)
def pbi_admin_raw(context: AssetExecutionContext) -> None:
    context.log.info("Fetching Power BI Bearer token via MSAL...")
    token = fetch_pbi_token()
    context.log.info("Token obtained.")

    # ── Fetch group IDs up front for the unused-artifacts endpoint ────────────
    context.log.info("Fetching group list for unused-artifacts endpoint...")
    group_ids: list[str] = []
    skip = 0
    while True:
        payload = _get(token, "/groups", {"$top": _GROUPS_PAGE_SIZE, "$skip": skip})
        batch = payload.get("value", [])
        if not batch:
            break
        group_ids.extend(g["id"] for g in batch)
        if len(batch) < _GROUPS_PAGE_SIZE:
            break
        skip += _GROUPS_PAGE_SIZE
    context.log.info(f"Found {len(group_ids)} workspaces for unused-artifacts sweep.")

    # ── Run all resources in a single dlt pipeline ────────────────────────────
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
            unused_artifacts_resource(token=token, group_ids=group_ids),
        ]
    )
    context.log.info(f"Load complete: {load_info}")
