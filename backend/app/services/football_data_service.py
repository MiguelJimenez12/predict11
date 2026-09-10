import os
import time
from threading import Lock

import httpx
from dotenv import load_dotenv

from app.services.football_api_service import _ssl_context

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"
CACHE_SECONDS = int(os.getenv("FOOTBALL_DATA_CACHE_SECONDS", "300"))
_cache: dict[str, tuple[float, dict]] = {}
_cache_lock = Lock()


def _get(endpoint: str, params: dict | None = None) -> dict:
    token = os.getenv("FOOTBALL_DATA_TOKEN")
    if not token:
        raise RuntimeError(
            "FOOTBALL_DATA_TOKEN no esta configurado. Obten uno gratis en football-data.org."
        )

    params = params or {}
    cache_key = f"{endpoint}:{sorted(params.items())}"
    now = time.monotonic()
    with _cache_lock:
        cached = _cache.get(cache_key)
        if cached and now - cached[0] < CACHE_SECONDS:
            return cached[1]

    response = httpx.get(
        f"{BASE_URL}/{endpoint.lstrip('/')}",
        headers={"X-Auth-Token": token},
        params=params,
        timeout=30,
        verify=_ssl_context(),
    )
    if response.status_code == 429:
        raise RuntimeError("Limite gratuito alcanzado. Espera un minuto e intenta de nuevo.")
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        message = response.json().get("message", "Error del proveedor de datos.")
        raise RuntimeError(message) from error
    data = response.json()

    with _cache_lock:
        _cache[cache_key] = (now, data)
    return data


def get_teams(competition_code: str) -> list[dict]:
    return _get(f"competitions/{competition_code}/teams").get("teams", [])


def get_matches(
    competition_code: str,
    *,
    status: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    params = {
        key: value
        for key, value in {
            "status": status,
            "dateFrom": date_from,
            "dateTo": date_to,
        }.items()
        if value
    }
    return _get(f"competitions/{competition_code}/matches", params).get("matches", [])


def get_standings(competition_code: str) -> dict:
    return _get(f"competitions/{competition_code}/standings")


def get_match(match_id: int) -> dict:
    return _get(f"matches/{match_id}")
