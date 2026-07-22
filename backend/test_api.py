from app.services.football_api_service import get_matches

matches = get_matches(2289)

print(len(matches))
print(matches[0])