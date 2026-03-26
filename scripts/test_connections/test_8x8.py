"""
Test script — 8x8 Work Analytics API connectivity.

Loads credentials from the project .env file and makes a single minimal API
call to verify connectivity, authentication, and that data is returned.

Usage (from the project root, with the venv active):
    python scripts/test_connections/test_8x8.py

What it does:
  - Queries CDR data for each PBX in dbt_project/seeds/8x8/pbx_country_mapping.csv
  - Uses a window of the last 7 days and pageSize=5 so the call is fast
  - Prints the HTTP status, record count, and the first record for each PBX
  - Prints a clear error message if authentication fails or the PBX is not found
"""

import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

# ── Load .env from the project root ──────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL   = os.environ.get("EIGHT_X_EIGHT_BASE_URL", "").rstrip("/")
API_KEY    = os.environ.get("EIGHT_X_EIGHT_API_KEY", "")
ENDPOINT   = "/api/analytics/report/external/v2/call-records"
PBX_CSV    = PROJECT_ROOT / "dbt_project" / "seeds" / "8x8" / "pbx_country_mapping.csv"

# Test window: last 7 days in CET
import zoneinfo
_CET = zoneinfo.ZoneInfo("Europe/Paris")
_now  = datetime.now(_CET)
_from = _now - timedelta(days=7)
WINDOW_START = _from.strftime("%Y-%m-%d %H:%M:%S")
WINDOW_END   = _now.strftime("%Y-%m-%d %H:%M:%S")


def check_env() -> bool:
    missing = [v for v in ("EIGHT_X_EIGHT_BASE_URL", "EIGHT_X_EIGHT_API_KEY") if not os.environ.get(v)]
    if missing:
        print(f"[ERROR] Missing required environment variables: {', '.join(missing)}")
        print(f"        Make sure {PROJECT_ROOT / '.env'} exists and contains these values.")
        return False
    return True


def load_pbx_list() -> list[tuple[str, str]]:
    with open(PBX_CSV, newline="", encoding="utf-8") as f:
        return [(r["pbx_id"].strip(), r["country"].strip()) for r in csv.DictReader(f) if r["pbx_id"].strip()]


def test_pbx(pbx_id: str, country: str) -> bool:
    print(f"\n  PBX: {pbx_id} ({country})")
    print(f"  Window: {WINDOW_START}  →  {WINDOW_END} (CET)")

    try:
        response = requests.get(
            f"{BASE_URL}{ENDPOINT}",
            headers={"8x8-apikey": API_KEY},
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
        print(f"  [ERROR] Could not connect to {BASE_URL}: {e}")
        return False

    print(f"  HTTP {response.status_code}")

    if not response.ok:
        print(f"  [FAIL] {response.text[:400]}")
        return False

    payload = response.json()
    total   = payload.get("meta", {}).get("totalRecordCount", "unknown")
    records = payload.get("data", [])

    print(f"  Total records in window: {total}")
    print(f"  Records returned (max 5): {len(records)}")

    if records:
        print("  First record:")
        print("  " + json.dumps(records[0], indent=4).replace("\n", "\n  "))
    else:
        print("  No records found in this window (no calls in the last 7 days, or PBX has no data).")

    return True


def main():
    print("=" * 60)
    print("8x8 API connectivity test")
    print("=" * 60)

    if not check_env():
        sys.exit(1)

    print(f"\nBase URL : {BASE_URL}")
    print(f"API key  : {API_KEY[:6]}{'*' * (len(API_KEY) - 6)}")

    pbx_list = load_pbx_list()
    print(f"\nTesting {len(pbx_list)} PBX(es) from pbx_country_mapping.csv...")

    results = []
    for pbx_id, country in pbx_list:
        ok = test_pbx(pbx_id, country)
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
