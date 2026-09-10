from dataclasses import dataclass


@dataclass(frozen=True)
class LeagueConfig:
    slug: str
    name: str
    country: str
    provider: str
    provider_code: str
    historical_code: str | None = None


LEAGUES = {
    league.slug: league
    for league in (
        LeagueConfig("premier-league", "Premier League", "England", "football-data", "PL", "E0"),
        LeagueConfig("la-liga", "LaLiga", "Spain", "football-data", "PD", "SP1"),
        LeagueConfig("serie-a", "Serie A", "Italy", "football-data", "SA", "I1"),
        LeagueConfig("bundesliga", "Bundesliga", "Germany", "football-data", "BL1", "D1"),
        LeagueConfig("ligue-1", "Ligue 1", "France", "football-data", "FL1", "F1"),
        LeagueConfig("champions-league", "UEFA Champions League", "Europe", "football-data", "CL"),
        LeagueConfig("liga-mx", "Liga MX", "Mexico", "api-football", "262"),
    )
}


def get_league(slug: str) -> LeagueConfig:
    try:
        return LEAGUES[slug]
    except KeyError as error:
        raise ValueError(f"Liga no soportada: {slug}") from error
