from app.config.leagues import LEAGUES, get_league
from app.schemas.league import League, LeagueMatch, LeagueStanding, LeagueTeam
from app.services import football_data_service
from app.services.standings_service import get_standings as get_liga_mx_standings
from app.services.team_service import get_teams as get_liga_mx_teams


def list_leagues() -> list[League]:
    return [
        League(
            slug=item.slug,
            name=item.name,
            country=item.country,
            provider=item.provider,
            prediction_model="historical-ml" if item.historical_code else "statistical",
        )
        for item in LEAGUES.values()
    ]


def list_teams(slug: str) -> list[LeagueTeam]:
    league = get_league(slug)
    if league.provider == "api-football":
        return [LeagueTeam(id=team.id, name=team.name, crest=team.logo) for team in get_liga_mx_teams()]

    return [
        LeagueTeam(
            id=team["id"],
            name=team["name"],
            short_name=team.get("shortName"),
            crest=team.get("crest"),
        )
        for team in football_data_service.get_teams(league.provider_code)
    ]


def list_matches(
    slug: str,
    *,
    status: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[LeagueMatch]:
    league = get_league(slug)
    if league.provider != "football-data":
        raise ValueError("La agenda multi-liga aun no esta disponible para Liga MX.")

    matches = football_data_service.get_matches(
        league.provider_code,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )
    return [
        LeagueMatch(
            id=match["id"],
            utc_date=match["utcDate"],
            status=match["status"],
            matchday=match.get("matchday"),
            home_team=LeagueTeam(
                id=match["homeTeam"]["id"],
                name=match["homeTeam"]["name"],
                short_name=match["homeTeam"].get("shortName"),
                crest=match["homeTeam"].get("crest"),
            ),
            away_team=LeagueTeam(
                id=match["awayTeam"]["id"],
                name=match["awayTeam"]["name"],
                short_name=match["awayTeam"].get("shortName"),
                crest=match["awayTeam"].get("crest"),
            ),
            home_score=match["score"]["fullTime"].get("home"),
            away_score=match["score"]["fullTime"].get("away"),
        )
        for match in matches
    ]


def standings(slug: str) -> list[LeagueStanding]:
    league = get_league(slug)
    if league.provider == "api-football":
        return [
            LeagueStanding(
                position=item.position,
                team=LeagueTeam(id=item.team_id, name=item.team_name, crest=item.team_logo),
                played_games=item.played,
                won=item.win,
                draw=item.draw,
                lost=item.lose,
                points=item.points,
                goals_for=item.goals_for,
                goals_against=item.goals_against,
                goal_difference=item.goal_difference,
            )
            for item in get_liga_mx_standings()
        ]

    data = football_data_service.get_standings(league.provider_code)
    total = next((item for item in data.get("standings", []) if item["type"] == "TOTAL"), None)
    if total is None:
        return []
    return [
        LeagueStanding(
            position=row["position"],
            team=LeagueTeam(
                id=row["team"]["id"],
                name=row["team"]["name"],
                short_name=row["team"].get("shortName"),
                crest=row["team"].get("crest"),
            ),
            played_games=row["playedGames"],
            won=row["won"],
            draw=row["draw"],
            lost=row["lost"],
            points=row["points"],
            goals_for=row["goalsFor"],
            goals_against=row["goalsAgainst"],
            goal_difference=row["goalDifference"],
        )
        for row in total["table"]
    ]
