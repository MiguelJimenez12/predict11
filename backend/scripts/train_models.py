import argparse
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.config.leagues import LEAGUES  # noqa: E402
from app.ml.historical_model import parse_csv, save_artifact, train  # noqa: E402
from app.services.football_api_service import _ssl_context  # noqa: E402

SEASONS = (
    ("1920", "2019-20"),
    ("2021", "2020-21"),
    ("2122", "2021-22"),
    ("2223", "2022-23"),
    ("2324", "2023-24"),
)
PRIMARY_URL = "https://www.football-data.co.uk/mmz4281/{season}/{code}.csv"
MIRROR_URL = "https://raw.githubusercontent.com/footballcsv/cache.footballdata/master/{season}/{code}.csv"
MIRROR_CODES = {"E0": "eng.1", "SP1": "es.1", "I1": "it.1", "D1": "de.1", "F1": "fr.1"}


def download_matches(code: str):
    matches = []
    primary_available = True
    with httpx.Client(timeout=30, verify=_ssl_context(), follow_redirects=True) as client:
        for primary_season, mirror_season in SEASONS:
            season_matches = []
            if primary_available:
                response = client.get(PRIMARY_URL.format(season=primary_season, code=code))
                season_matches = parse_csv(response.text) if response.status_code == 200 else []
                primary_available = bool(season_matches)
            if not season_matches:
                response = client.get(MIRROR_URL.format(season=mirror_season, code=MIRROR_CODES[code]))
                season_matches = parse_csv(response.text) if response.status_code == 200 else []
            matches.extend(season_matches)
    return matches


def main():
    parser = argparse.ArgumentParser(description="Entrena y evalua los modelos historicos de Predict11.")
    parser.add_argument("--league", choices=[slug for slug, item in LEAGUES.items() if item.historical_code])
    args = parser.parse_args()
    selected = [LEAGUES[args.league]] if args.league else [item for item in LEAGUES.values() if item.historical_code]

    for league in selected:
        matches = download_matches(league.historical_code)
        if len(matches) < 100:
            raise RuntimeError(f"Datos insuficientes para {league.name}: {len(matches)} partidos")
        weights, states, metrics, split = train(matches)
        output = ROOT / "ml_models" / f"{league.slug}.json"
        data_through = max(match.date for match in matches).date().isoformat()
        save_artifact(output, league.slug, weights, states, metrics, len(matches), split, data_through)
        print(f"{league.name}: {len(matches)} partidos, accuracy={metrics['accuracy']}, log_loss={metrics['log_loss']}")


if __name__ == "__main__":
    main()
