"""
Shared authentication helpers for 8x8 API assets.

Both the Analytics (CDR) and Admin Provisioning (Users) APIs use the same
OAuth2 token exchange flow via the Analytics token endpoint.
"""

import os

import requests

_TOKEN_PATH = "/analytics/work/v1/oauth/token"
_TIMEOUT = 60


def fetch_token() -> str:
    """
    Exchange username + password for a Bearer token via POST /v1/oauth/token.
    Returns the access_token string (valid for 30 minutes).
    """
    base_url = os.environ["EIGHT_X_EIGHT_BASE_URL"].rstrip("/")
    response = requests.post(
        f"{base_url}{_TOKEN_PATH}",
        headers={"8x8-apikey": os.environ["EIGHT_X_EIGHT_API_KEY"]},
        data={
            "username": os.environ["EIGHT_X_EIGHT_USERNAME"],
            "password": os.environ["EIGHT_X_EIGHT_PASSWORD"],
        },
        timeout=_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["access_token"]
