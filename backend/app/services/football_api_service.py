import os
import ssl

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = int(os.getenv("FOOTBALL_LEAGUE_ID", "262"))
SEASON = int(os.getenv("FOOTBALL_SEASON", "2024"))


def _ssl_context():
    """Use Windows trusted roots in Python installations that do not load them."""
    context = ssl.create_default_context()
    if hasattr(ssl, "VERIFY_X509_STRICT"):
        context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    if os.name == "nt" and hasattr(ssl, "enum_certificates"):
        for certificate, encoding, trust in ssl.enum_certificates("ROOT"):
            if encoding == "x509_asn":
                try:
                    context.load_verify_locations(
                        cadata=ssl.DER_cert_to_PEM_cert(certificate)
                    )
                except ssl.SSLError:
                    continue
    return context


def _get(endpoint: str, params: dict):
    api_key = os.getenv("FOOTBALL_API_KEY")
    if not api_key:
        raise RuntimeError(
            "FOOTBALL_API_KEY no esta configurada. Copia .env.example a .env."
        )

    response = httpx.get(
        f"{BASE_URL}/{endpoint}",
        headers={"x-apisports-key": api_key},
        params=params,
        timeout=30.0,
        verify=_ssl_context(),
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
            "league": LEAGUE_ID,
            "season": SEASON
        }
    )

    return data["response"]


def get_matches(team_id: int, season: int = SEASON):

    data = _get(
        "fixtures",
        {
            "league": LEAGUE_ID,
            "season": season,
            "team": team_id
        }
    )

    return data["response"]


def get_standings():

    data = _get(
        "standings",
        {
            "league": LEAGUE_ID,
            "season": SEASON
        }
    )

    return data["response"][0]["league"]["standings"][0]


def get_statistics(team_id: int):

    data = _get(
        "teams/statistics",
        {
            "league": LEAGUE_ID,
            "season": SEASON,
            "team": team_id
        }
    )

    return data["response"]


def get_head_to_head(home_team: int, away_team: int):

    data = _get(
        "fixtures/headtohead",
        {
            "h2h": f"{home_team}-{away_team}"
        }
    )

    return data["response"]
