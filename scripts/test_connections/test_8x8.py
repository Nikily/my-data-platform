"""
Test script — 8x8 Work Analytics API connectivity.

Loads credentials from the project .env file, obtains a Bearer token via the
OAuth2 token endpoint, then makes a minimal CDR API call per PBX to verify
that the full auth flow and data retrieval work end-to-end.

Usage (from the project root, with the venv active):
    python scripts/test_connections/test_8x8.py
"""

import csv
import json
import sys
import zoneinfo
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

# ── Load .env ─────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL = os.environ.get("EIGHT_X_EIGHT_BASE_URL", "").rstrip("/")
API_KEY  = os.environ.get("EIGHT_X_EIGHT_API_KEY", "")
USERNAME      = os.environ.get("EIGHT_X_EIGHT_USERNAME", "")
PASSWORD      = os.environ.get("EIGHT_X_EIGHT_PASSWORD", "")

TOKEN_PATH = "/analytics/work/v1/oauth/token"
CDR_PATH   = "/analytics/work/v2/call-records"
PBX_CSV    = PROJECT_ROOT / "dbt_project" / "seeds" / "8x8" / "pbx_country_mapping.csv"

_CET  = zoneinfo.ZoneInfo("Europe/Paris")
_now  = datetime.now(_CET)
_from = _now - timedelta(days=7)
WINDOW_START = _from.strftime("%Y-%m-%d %H:%M:%S")
WINDOW_END   = _now.strftime("%Y-%m-%d %H:%M:%S")


def check_env() -> bool:
    required = {
        "EIGHT_X_EIGHT_BASE_URL":  BASE_URL,
        "EIGHT_X_EIGHT_API_KEY":   API_KEY,
        "EIGHT_X_EIGHT_USERNAME":  USERNAME,
        "EIGHT_X_EIGHT_PASSWORD":  PASSWORD,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"[ERROR] Missing environment variables: {', '.join(missing)}")
        print(f"        Check {PROJECT_ROOT / '.env'}")
        return False
    return True


def load_pbx_list() -> list[tuple[str, str]]:
    with open(PBX_CSV, newline="", encoding="utf-8") as f:
        return [(r["pbx_id"].strip(), r["country"].strip()) for r in csv.DictReader(f) if r["pbx_id"].strip()]


def fetch_token() -> str | None:
    """POST to the token endpoint and return the access_token."""
    print(f"\nStep 1 — Fetching Bearer token")
    print(f"  URL      : {BASE_URL}{TOKEN_PATH}")
    print(f"  Username : {USERNAME}")

    try:
        response = requests.post(
            f"{BASE_URL}{TOKEN_PATH}",
            headers={"8x8-apikey": API_KEY},
            data={"username": USERNAME, "password": PASSWORD},
            timeout=30,
        )
    except requests.exceptions.ConnectionError as e:
        print(f"  [ERROR] Could not connect: {e}")
        return None

    print(f"  HTTP {response.status_code}")

    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return None

    token = response.json().get("access_token")
    expires_in = response.json().get("expires_in", "?")
    print(f"  Token obtained (expires in {expires_in}s): {token[:30]}...")
    return token


def test_pbx(pbx_id: str, country: str, token: str) -> bool:
    print(f"\n  PBX : {pbx_id} ({country})")
    print(f"  URL : {BASE_URL}{CDR_PATH}")
    print(f"  Window: {WINDOW_START}  →  {WINDOW_END} (CET, last 7 days)")

    try:
        response = requests.get(
            f"{BASE_URL}{CDR_PATH}",
            headers={"Authorization": f"Bearer {token}", "8x8-apikey": API_KEY},
            params={
                "pbxId":     pbx_id,
                "startTime": WINDOW_START,
                "endTime":   WINDOW_END,
                "timeZone":  "Europe/Paris",
                "pageSize":  5,
            },
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
    total   = payload.get("meta", {}).get("totalRecordCount", "unknown")
    records = payload.get("data", [])

    print(f"  Total records in window : {total}")
    print(f"  Records returned (max 5): {len(records)}")

    if records:
        print("  First record:")
        print("  " + json.dumps(records[0], indent=4).replace("\n", "\n  "))
    else:
        print("  No records found in this window.")

    return True


def main():
    print("=" * 60)
    print("8x8 API connectivity test")
    print("=" * 60)

    if not check_env():
        sys.exit(1)

    print(f"\nBase URL : {BASE_URL}")
    print(f"API key  : {API_KEY[:6]}{'*' * (len(API_KEY) - 6)}")

    token = fetch_token()
    if not token:
        sys.exit(1)

    pbx_list = load_pbx_list()
    print(f"\nStep 2 — Testing {len(pbx_list)} PBX(es)")

    results = []
    for pbx_id, country in pbx_list:
        ok = test_pbx(pbx_id, country, token)
        results.append((pbx_id, country, ok))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    for pbx_id, country, ok in results:
        status = "OK  " if ok else "FAIL"
        print(f"  [{status}]  {pbx_id} ({country})")

    if not all(ok for _, _, ok in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
