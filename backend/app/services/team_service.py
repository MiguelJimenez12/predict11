def get_all_teams():
    """
    Returns the list of available teams.
    """

    teams = [
        {"id": 1, "name": "Pumas UNAM"},
        {"id": 2, "name": "Club América"},
        {"id": 3, "name": "Cruz Azul"},
        {"id": 4, "name": "Tigres UANL"},
    ]

    return teams

def get_team_by_id(team_id: int):
    teams = get_all_teams()

    for team in teams:
        if team["id"] == team_id:
            return team

    return None