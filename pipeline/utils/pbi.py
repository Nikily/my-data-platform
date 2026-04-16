"""
Shared authentication helper for Power BI Admin REST API assets.

Uses MSAL client credentials flow (service principal) to obtain a
Bearer token scoped to the Power BI API.
"""

import os

import msal

_PBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"


def fetch_pbi_token() -> str:
    """
    Obtain a Bearer token via MSAL client credentials flow.
    Reads AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET from the environment.
    Returns the access_token string (valid for ~1 hour).
    """
    app = msal.ConfidentialClientApplication(
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_credential=os.environ["AZURE_CLIENT_SECRET"],
        token_cache=None,
        authority=f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}",
    )
    result = app.acquire_token_for_client(scopes=[_PBI_SCOPE])
    if "access_token" not in result:
        raise RuntimeError(f"Failed to obtain Power BI token: {result}")
    return result["access_token"]
