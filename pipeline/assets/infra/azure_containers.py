"""
Azure Blob Storage container provisioning asset.

Ensures required containers exist before ingestion assets run.
Uses the service principal credentials (AZURE_TENANT_ID, AZURE_CLIENT_ID,
AZURE_CLIENT_SECRET) configured in .env.
"""

import os

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dagster import AssetExecutionContext, asset


def _blob_service_client() -> BlobServiceClient:
    credential = ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
    )
    account_url = (
        f"https://{os.environ['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net"
    )
    return BlobServiceClient(account_url=account_url, credential=credential)


@asset(
    group_name="infra",
    kinds={"azure"},
    description=(
        "Ensures the Azure Blob Storage container for 8x8 CDR data exists. "
        "Creates it if absent. Container name is read from EIGHT_X_EIGHT_CONTAINER."
    ),
)
def azure_container_8x8(context: AssetExecutionContext) -> None:
    container = os.environ["EIGHT_X_EIGHT_CONTAINER"]
    client = _blob_service_client()
    container_client = client.get_container_client(container)

    if container_client.exists():
        context.log.info(f"Container '{container}' already exists.")
    else:
        container_client.create_container()
        context.log.info(f"Created container '{container}'.")
