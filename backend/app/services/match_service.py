def get_all_matches():
    return [
        {
            "id": 1,
            "home_team_id": 1,
            "away_team_id": 2,
            "date": "2026-07-20",
            "competition": "Liga MX",
            "round": 3,
            "stadium": "Estadio Olímpico Universitario",
            "home_score": None,
            "away_score": None,
            "status": "scheduled"
        },
        {
            "id": 2,
            "home_team_id": 3,
            "away_team_id": 4,
            "date": "2026-07-21",
            "competition": "Liga MX",
            "round": 3,
            "stadium": "Estadio Akron",
            "home_score": None,
            "away_score": None,
            "status": "scheduled"
        },
        {
            "id": 3,
            "home_team_id": 2,
            "away_team_id": 1,
            "date": "2026-07-28",
            "competition": "Liga MX",
            "round": 4,
            "stadium": "Estadio Ciudad de los Deportes",
            "home_score": None,
            "away_score": None,
            "status": "scheduled"
        }
    ]


def get_match_by_id(match_id: int):
    matches = get_all_matches()

    for match in matches:
        if match["id"] == match_id:
            return match

    return None