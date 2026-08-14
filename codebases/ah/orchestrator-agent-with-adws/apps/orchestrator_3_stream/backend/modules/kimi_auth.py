"""
Kimi Code (Moonshot) OAuth token keeper.

The Kimi Code subscription authenticates with a short-lived (~15 min) OAuth
access token stored in ~/.kimi-code/credentials/kimi-code.json and refreshed via
a rotating refresh token. The Claude Agent SDK forwards ANTHROPIC_AUTH_TOKEN to
the underlying `claude` CLI, so for agents to keep working we must keep that env
var pointed at a fresh access token.

This module refreshes the token (OAuth refresh_token grant against auth.kimi.com),
persists the rotated tokens back to the shared credentials file (so the official
`kimi` CLI keeps working too), and updates os.environ["ANTHROPIC_AUTH_TOKEN"].

Only used when ANTHROPIC_BASE_URL points at the Kimi coding endpoint.

IMPORTANT: fails loud — every error is logged; the caller keeps the previous
token rather than silently dropping auth.
"""

import os
import json
import time
import asyncio
import shutil
import tempfile
import urllib.request
import urllib.parse
from pathlib import Path

from .config import config_logger

TOKEN_URL = os.getenv("KIMI_TOKEN_URL", "https://auth.kimi.com/api/oauth/token")
# Public OAuth client id for Kimi Code (embedded in the access-token JWT claims).
CLIENT_ID = os.getenv("KIMI_CLIENT_ID", "17e5f671-d194-4dfb-9706-5516cb48c098")
CREDS_PATH = Path(
    os.getenv(
        "KIMI_CREDENTIALS_FILE",
        str(Path.home() / ".kimi-code" / "credentials" / "kimi-code.json"),
    )
)
# Refresh when fewer than this many seconds remain on the access token.
REFRESH_MARGIN_SECONDS = int(os.getenv("KIMI_REFRESH_MARGIN", "300"))


def is_enabled() -> bool:
    """True when the app is configured for Kimi and a credentials file exists."""
    base = os.getenv("ANTHROPIC_BASE_URL", "")
    return "kimi.com" in base and CREDS_PATH.exists()


def _read_creds() -> dict:
    with open(CREDS_PATH) as f:
        return json.load(f)


def _write_creds(data: dict) -> None:
    """Atomically write the credentials file (same dir temp + os.replace)."""
    fd, tmp = tempfile.mkstemp(dir=str(CREDS_PATH.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        os.replace(tmp, CREDS_PATH)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _http_refresh(refresh_token: str) -> dict:
    body = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
        }
    ).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        headers={"content-type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def ensure_fresh_token(force: bool = False) -> str | None:
    """
    Ensure the credentials file holds a valid access token and export it via
    os.environ["ANTHROPIC_AUTH_TOKEN"]. Refreshes (and persists rotation) when the
    current token is within REFRESH_MARGIN_SECONDS of expiry (or force=True).

    Returns the current access token, or None if unavailable.
    """
    try:
        creds = _read_creds()
    except Exception as e:
        config_logger.warning(f"[kimi_auth] cannot read credentials {CREDS_PATH}: {e}")
        return None

    now = time.time()
    try:
        exp = float(creds.get("expires_at") or 0)
    except (TypeError, ValueError):
        exp = 0.0
    token = creds.get("access_token")

    if token and not force and (exp - now) > REFRESH_MARGIN_SECONDS:
        os.environ["ANTHROPIC_AUTH_TOKEN"] = token
        return token

    refresh_token = creds.get("refresh_token")
    if not refresh_token:
        config_logger.error("[kimi_auth] no refresh_token in credentials; cannot refresh")
        if token:
            os.environ["ANTHROPIC_AUTH_TOKEN"] = token
        return token

    try:
        resp = _http_refresh(refresh_token)
    except Exception as e:
        config_logger.error(f"[kimi_auth] token refresh failed: {e}")
        if token:
            os.environ["ANTHROPIC_AUTH_TOKEN"] = token  # keep old until it truly dies
        return token

    new_token = resp.get("access_token")
    if not new_token:
        config_logger.error(f"[kimi_auth] refresh response missing access_token: {resp}")
        if token:
            os.environ["ANTHROPIC_AUTH_TOKEN"] = token
        return token

    creds["access_token"] = new_token
    if resp.get("refresh_token"):
        creds["refresh_token"] = resp["refresh_token"]  # persist rotation
    if resp.get("expires_in"):
        try:
            creds["expires_in"] = resp["expires_in"]
            creds["expires_at"] = now + float(resp["expires_in"])
        except (TypeError, ValueError):
            pass
    for k in ("scope", "token_type"):
        if resp.get(k):
            creds[k] = resp[k]

    try:
        _write_creds(creds)
    except Exception as e:
        config_logger.error(f"[kimi_auth] could not persist refreshed credentials: {e}")

    os.environ["ANTHROPIC_AUTH_TOKEN"] = new_token
    config_logger.info(
        f"[kimi_auth] refreshed Kimi token (valid ~{int(resp.get('expires_in', 0))}s)"
    )
    return new_token


async def refresh_loop(interval_seconds: int = 120) -> None:
    """Background loop that keeps the Kimi access token fresh for the process."""
    config_logger.info(
        f"[kimi_auth] token refresh loop started (every {interval_seconds}s, "
        f"margin {REFRESH_MARGIN_SECONDS}s)"
    )
    while True:
        try:
            ensure_fresh_token()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            config_logger.error(f"[kimi_auth] refresh loop iteration error: {e}")
        await asyncio.sleep(interval_seconds)
