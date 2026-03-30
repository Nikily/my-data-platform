"""
show_container_details.py — Print Azure Blob Storage connection details for a container.

Usage:
    source .venv/bin/activate
    python scripts/show_container_details.py

Reads credentials from .env. Defaults to EIGHT_X_EIGHT_CONTAINER but accepts
an optional container name as argument:
    python scripts/show_container_details.py my-other-container
"""

import os
import sys
from pathlib import Path

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

container_name = sys.argv[1] if len(sys.argv) > 1 else os.environ["EIGHT_X_EIGHT_CONTAINER"]

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"],
)

account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
account_url = f"https://{account_name}.blob.core.windows.net"

client = BlobServiceClient(account_url=account_url, credential=credential)
container_client = client.get_container_client(container_name)

if not container_client.exists():
    print(f"Container '{container_name}' does not exist.")
    sys.exit(1)

props = container_client.get_container_properties()

print()
print("=" * 60)
print(f"  Container: {container_name}")
print("=" * 60)
print()
print("── Power BI / Azure Storage connection details ──────────────")
print(f"  Account name   : {account_name}")
print(f"  Container name : {container_name}")
print(f"  Blob endpoint  : {account_url}")
print(f"  Container URL  : {account_url}/{container_name}")
print()
print("── Authentication (service principal) ───────────────────────")
print(f"  Tenant ID      : {os.environ['AZURE_TENANT_ID']}")
print(f"  Client ID      : {os.environ['AZURE_CLIENT_ID']}")
print(f"  Client secret  : {'*' * 6} (see .env → AZURE_CLIENT_SECRET)")
print()
print("── Container properties ──────────────────────────────────────")
print(f"  Last modified  : {props['last_modified']}")
print(f"  Public access  : {props['public_access'] or 'None (private)'}")
print(f"  Lease state    : {props['lease']['state']}")
print()
print("── Blobs ─────────────────────────────────────────────────────")
blobs = list(container_client.list_blobs())
if blobs:
    for blob in blobs:
        size_kb = blob["size"] / 1024
        print(f"  {blob['name']:<50} {size_kb:>10.1f} KB")
else:
    print("  (no blobs yet)")
print()
