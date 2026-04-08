"""
Test script — Power BI Admin REST API connectivity.

Loads credentials from the project .env file, obtains a Bearer token via the
Microsoft identity platform (OAuth2 client credentials flow), then calls the
Admin - Apps GetAppsAsAdmin endpoint to verify end-to-end connectivity.

Usage (from the project root, with the venv active):
    python scripts/test_connections/test_pbi_admin.py
"""

import json
import os
import sys
import msal
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Load .env ─────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN_URL  = os.environ.get("PBI_REST_API_TOKEN_URL", "").rstrip("/")
BASE_URL   = os.environ.get("PBI_REST_API_BASE_URL", "").rstrip("/")
TENANT_ID  = os.environ.get("AZURE_TENANT_ID", "")
CLIENT_ID  = os.environ.get("AZURE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "")

APPS_PATH  = "/v1.0/myorg/admin/apps"
# Power BI REST API resource scope for client credentials flow
PBI_SCOPE  = "https://analysis.windows.net/powerbi/api/.default"

# -------------------------------
# TOKEN ACQUISITION FUNCTION
# -------------------------------
def get_token(scope):
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        token_cache=None,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
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


def test_get_apps(token: str) -> bool:
    """Call Admin - Apps GetAppsAsAdmin and print the first few results."""
    url = f"{BASE_URL}{APPS_PATH}"
    print(f"\nStep 2 — GET {url}")
    print(f"  $top=10")

    try:
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={"$top": 10},
            timeout=30,
        )
    except requests.exceptions.ConnectionError as e:
        print(f"  [ERROR] Could not connect: {e}")
        return False

    print(f"  HTTP {response.status_code}")

    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False

    payload = response.json()
    apps = payload.get("value", [])

    print(f"  Apps returned: {len(apps)}")

    if apps:
        print("  First app:")
        print("  " + json.dumps(apps[0], indent=4).replace("\n", "\n  "))
    else:
        print("  No apps found in the organisation.")

    return True


def main():
    print("=" * 60)
    print("Power BI Admin REST API connectivity test")
    print("=" * 60)

    if not check_env():
        sys.exit(1)

    print(f"\nBase URL  : {BASE_URL}")
    print(f"Tenant ID : {TENANT_ID}")
    print(f"Client ID : {CLIENT_ID}")
    print(f"Client secret: {'*' * 6}{CLIENT_SECRET[-4:]}")

    token = fetch_token()
    if not token:
        sys.exit(1)

    ok = test_get_apps(token)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  [{'OK  ' if ok else 'FAIL'}]  Admin - Apps GetAppsAsAdmin")

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
