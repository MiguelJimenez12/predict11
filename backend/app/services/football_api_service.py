import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


def _get(endpoint: str, params: dict):

    response = httpx.get(
        f"{BASE_URL}/{endpoint}",
        headers=HEADERS,
        params=params,
        timeout=30.0
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise Exception(data["errors"])

    return data


def get_teams():

    data = _get(
        "teams",
        {
            "league": 262,
            "season": 2024
        }
    )

    return data["response"]


def get_matches(team_id: int, season: int = 2024):

    data = _get(
        "fixtures",
        {
            "league": 262,
            "season": season,
            "team": team_id
        }
    )

    return data["response"]


def get_standings():

    data = _get(
        "standings",
        {
            "league": 262,
            "season": 2024
        }
    )

    return data["response"][0]["league"]["standings"][0]

def get_head_to_head(home_team: int, away_team: int):

    data = _get(
        "fixtures/headtohead",
        {
            "h2h": f"{home_team}-{away_team}"
        }
    )

    return data["response"]