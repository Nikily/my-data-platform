"""
Installs and persists the DuckDB extensions required by the platform.

Run this script once after setting up the virtual environment:
    .venv/bin/python scripts/install_duckdb_extensions.py

Extensions are installed into DuckDB's local extension cache (~/.duckdb/extensions)
and do not need to be reinstalled on every run. Subsequent LOAD calls in the
pipeline will use the cached versions.
"""

import duckdb

EXTENSIONS = ["azure", "delta"]

with duckdb.connect() as conn:
    for ext in EXTENSIONS:
        print(f"Installing extension: {ext} ...")
        conn.execute(f"INSTALL {ext};")
        conn.execute(f"LOAD {ext};")
        print(f"  OK")

print("\nAll DuckDB extensions installed successfully.")
