import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://v3.football.api-sports.io"


def get_teams():

    url = f"{BASE_URL}/teams"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "league": 262,
        "season": 2024
    }

    response = httpx.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]

def get_matches(team_id: int, season: int = 2024):

    url = f"{BASE_URL}/fixtures"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "league": 262,
        "season": season,
        "team": team_id
    }

    response = httpx.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]