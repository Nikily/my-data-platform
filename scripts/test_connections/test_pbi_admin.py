"""
Test script — Power BI Admin REST API connectivity.

Loads credentials from the project .env file, obtains a Bearer token via MSAL
(OAuth2 client credentials flow), then calls every Admin API endpoint to verify
end-to-end connectivity.

Endpoints tested:
  1. Admin - Apps GetAppsAsAdmin
  2. Admin - Get Capacities As Admin
  3. Admin - Get Refreshables
  4. Admin - Groups GetGroupsAsAdmin
  5. Admin - Dashboards GetDashboardsAsAdmin
  6. Admin - Reports GetReportsAsAdmin
  7. Admin - Datasets GetDatasetsAsAdmin
  8. Admin - WidelySharedArtifacts LinksSharedToWholeOrganization
  9. Admin - Groups GetUnusedArtifactsAsAdmin  (uses first group ID from step 4)

Usage (from the project root, with the venv active):
    python scripts/test_connections/test_pbi_admin.py
"""

import json
import msal
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Load .env ─────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN_URL     = os.environ.get("PBI_REST_API_TOKEN_URL", "").rstrip("/")
BASE_URL      = os.environ.get("PBI_REST_API_BASE_URL", "").rstrip("/")
TENANT_ID     = os.environ.get("AZURE_TENANT_ID", "")
CLIENT_ID     = os.environ.get("AZURE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "")

PBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"


# ── Auth ──────────────────────────────────────────────────────────────────────

def get_token(scope: str) -> str:
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        token_cache=None,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    )
    token = app.acquire_token_for_client(scopes=[scope])
    if "access_token" not in token:
        raise Exception(f"Failed to obtain token: {token}")
    return token["access_token"]


def check_env() -> bool:
    required = {
        "PBI_REST_API_BASE_URL": BASE_URL,
        "AZURE_TENANT_ID":       TENANT_ID,
        "AZURE_CLIENT_ID":       CLIENT_ID,
        "AZURE_CLIENT_SECRET":   CLIENT_SECRET,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"[ERROR] Missing environment variables: {', '.join(missing)}")
        print(f"        Check {PROJECT_ROOT / '.env'}")
        return False
    return True


def fetch_token() -> str | None:
    """Obtain a Bearer token via MSAL client credentials flow."""
    print("\nStep 1 — Fetching Bearer token")
    print(f"  Authority : https://login.microsoftonline.com/{TENANT_ID}")
    print(f"  Client ID : {CLIENT_ID}")
    print(f"  Scope     : {PBI_SCOPE}")
    try:
        token = get_token(PBI_SCOPE)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None
    print(f"  Token obtained: {token[:30]}...")
    return token


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get(token: str, path: str, params: dict | None = None) -> requests.Response | None:
    url = f"{BASE_URL}{path}"
    try:
        return requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=30,
        )
    except requests.exceptions.ConnectionError as e:
        print(f"  [ERROR] Could not connect: {e}")
        return None


def _print_first(items: list, label: str) -> None:
    print(f"  {label} returned: {len(items)}")
    if items:
        print("  First item:")
        print("  " + json.dumps(items[0], indent=4).replace("\n", "\n  "))
    else:
        print(f"  No {label.lower()} found.")


# ── Test functions ─────────────────────────────────────────────────────────────

def test_get_apps(token: str) -> bool:
    """GET /apps — Apps GetAppsAsAdmin"""
    print(f"\n[1] GET {BASE_URL}/apps")
    response = _get(token, "/apps", {"$top": 10})
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    _print_first(response.json().get("value", []), "Apps")
    return True


def test_get_capacities(token: str) -> bool:
    """GET /capacities — Get Capacities As Admin"""
    print(f"\n[2] GET {BASE_URL}/capacities")
    response = _get(token, "/capacities")
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    _print_first(response.json().get("value", []), "Capacities")
    return True


def test_get_refreshables(token: str) -> bool:
    """GET /capacities/refreshables — Get Refreshables"""
    print(f"\n[3] GET {BASE_URL}/capacities/refreshables")
    response = _get(token, "/capacities/refreshables", {"$top": 5})
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    _print_first(response.json().get("value", []), "Refreshables")
    return True


def test_get_groups(token: str) -> tuple[bool, str | None]:
    """GET /groups — Groups GetGroupsAsAdmin. Returns (ok, first_group_id)."""
    print(f"\n[4] GET {BASE_URL}/groups")
    response = _get(token, "/groups", {"$top": 10})
    if response is None:
        return False, None
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False, None
    groups = response.json().get("value", [])
    _print_first(groups, "Groups (workspaces)")
    first_id = groups[0]["id"] if groups else None
    return True, first_id


def test_get_dashboards(token: str) -> bool:
    """GET /dashboards — Dashboards GetDashboardsAsAdmin"""
    print(f"\n[5] GET {BASE_URL}/dashboards")
    response = _get(token, "/dashboards", {"$top": 5})
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    _print_first(response.json().get("value", []), "Dashboards")
    return True


def test_get_reports(token: str) -> bool:
    """GET /reports — Reports GetReportsAsAdmin"""
    print(f"\n[6] GET {BASE_URL}/reports")
    response = _get(token, "/reports", {"$top": 5})
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    _print_first(response.json().get("value", []), "Reports")
    return True


def test_get_datasets(token: str) -> bool:
    """GET /datasets — Datasets GetDatasetsAsAdmin"""
    print(f"\n[7] GET {BASE_URL}/datasets")
    response = _get(token, "/datasets", {"$top": 5})
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    _print_first(response.json().get("value", []), "Datasets")
    return True


def test_get_widely_shared(token: str) -> bool:
    """GET /widelySharedArtifacts/linksSharedToWholeOrganization"""
    print(f"\n[8] GET {BASE_URL}/widelySharedArtifacts/linksSharedToWholeOrganization")
    response = _get(token, "/widelySharedArtifacts/linksSharedToWholeOrganization")
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    entities = response.json().get("artifactAccessEntities", [])
    print(f"  Widely shared artifacts returned: {len(entities)}")
    if entities:
        print("  First item:")
        print("  " + json.dumps(entities[0], indent=4).replace("\n", "\n  "))
    else:
        print("  No widely shared artifacts found.")
    return True


def test_get_unused_artifacts(token: str, group_id: str) -> bool:
    """GET /groups/{groupId}/unused — Groups GetUnusedArtifactsAsAdmin"""
    print(f"\n[9] GET {BASE_URL}/groups/{group_id}/unused")
    response = _get(token, f"/groups/{group_id}/unused")
    if response is None:
        return False
    print(f"  HTTP {response.status_code}")
    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False
    entities = response.json().get("unusedArtifactEntities", [])
    print(f"  Unused artifacts returned: {len(entities)}")
    if entities:
        print("  First item:")
        print("  " + json.dumps(entities[0], indent=4).replace("\n", "\n  "))
    else:
        print("  No unused artifacts found in this workspace.")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Power BI Admin REST API connectivity test")
    print("=" * 60)

    if not check_env():
        sys.exit(1)

    print(f"\nBase URL     : {BASE_URL}")
    print(f"Tenant ID    : {TENANT_ID}")
    print(f"Client ID    : {CLIENT_ID}")
    print(f"Client secret: {'*' * 6}{CLIENT_SECRET[-4:]}")

    token = fetch_token()
    if not token:
        sys.exit(1)

    results: list[tuple[str, bool]] = []

    results.append(("Apps GetAppsAsAdmin",                              test_get_apps(token)))
    results.append(("Get Capacities As Admin",                         test_get_capacities(token)))
    results.append(("Get Refreshables",                                test_get_refreshables(token)))

    groups_ok, first_group_id = test_get_groups(token)
    results.append(("Groups GetGroupsAsAdmin",                         groups_ok))

    results.append(("Dashboards GetDashboardsAsAdmin",                 test_get_dashboards(token)))
    results.append(("Reports GetReportsAsAdmin",                       test_get_reports(token)))
    results.append(("Datasets GetDatasetsAsAdmin",                     test_get_datasets(token)))
    results.append(("WidelySharedArtifacts LinksSharedToWholeOrg",    test_get_widely_shared(token)))

    if first_group_id:
        results.append(("Groups GetUnusedArtifactsAsAdmin",            test_get_unused_artifacts(token, first_group_id)))
    else:
        print("\n[9] Skipping GetUnusedArtifactsAsAdmin — no group ID available from step 4.")
        results.append(("Groups GetUnusedArtifactsAsAdmin",            False))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    for name, ok in results:
        print(f"  [{'OK  ' if ok else 'FAIL'}]  {name}")

    if not all(ok for _, ok in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
