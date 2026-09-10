import csv
import json
import math
import random
import re
import unicodedata
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


OUTCOMES = ("home", "draw", "away")

TEAM_NAME_ALIASES = {
    "athleticclub": "athbilbao", "clubatleticodemadrid": "athmadrid", "caosasuna": "osasuna",
    "rcdespanyoldebarcelona": "espanol", "rayovallecanodemadrid": "vallecano",
    "realbetisbalompie": "betis", "realsociedaddefutbol": "sociedad", "deportivoalaves": "alaves",
    "rcceltadevig": "celta", "manchestercity": "mancity", "manchesterunited": "manunited",
    "nottinghamforest": "notmforest", "brightonhovealbion": "brighton", "acmilan": "milan",
    "acfiorentina": "fiorentina", "asroma": "roma", "atalantabc": "atalanta", "bolognafc1909": "bologna",
    "fcinternazionalemilano": "inter", "parmacalcio1913": "parma", "sscnapoli": "napoli",
    "ussassuolo": "sassuolo", "uslecce": "lecce", "1fckoln": "fckoln", "tsg1899hoffenheim": "hoffenheim",
    "bayer04leverkusen": "leverkusen", "fcbayernmunchen": "bayernmunich", "svwerderbremen": "werderbremen",
    "1fsvmainz05": "mainz", "borussiamonchengladbach": "mgladbach", "eintrachtfrankfurt": "einfrankfurt",
    "1fcunionberlin": "unionberlin", "stadebrestois29": "brest", "olympiquedemarseille": "marseille",
    "olympiquelyonnais": "lyon", "parissaintgermain": "parissg", "staderennaisfc1901": "rennes",
    "estroyesac": "troyes", "angerssco": "angers", "lehavreac": "lehavre",
    "racingclubdelens": "lens", "asmonaco": "monaco", "rcstrasbourgalsace": "strasbourg",
}


@dataclass
class MatchRecord:
    date: datetime
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int


@dataclass
class TeamState:
    elo: float = 1500.0
    recent_points: deque = field(default_factory=lambda: deque(maxlen=5))
    recent_goals_for: deque = field(default_factory=lambda: deque(maxlen=5))
    recent_goals_against: deque = field(default_factory=lambda: deque(maxlen=5))
    home_goal_diffs: deque = field(default_factory=lambda: deque(maxlen=10))
    away_goal_diffs: deque = field(default_factory=lambda: deque(maxlen=10))

    def serializable(self) -> dict:
        return {
            "elo": self.elo,
            "recent_points": list(self.recent_points),
            "recent_goals_for": list(self.recent_goals_for),
            "recent_goals_against": list(self.recent_goals_against),
            "home_goal_diffs": list(self.home_goal_diffs),
            "away_goal_diffs": list(self.away_goal_diffs),
        }


def _average(values, default=0.0):
    return sum(values) / len(values) if values else default


def _features(home: TeamState, away: TeamState) -> list[float]:
    return [
        1.0,
        (home.elo - away.elo) / 400.0,
        (_average(home.recent_points, 1.5) - _average(away.recent_points, 1.5)) / 3.0,
        (_average(home.recent_goals_for, 1.2) - _average(away.recent_goals_for, 1.2)) / 3.0,
        (_average(away.recent_goals_against, 1.2) - _average(home.recent_goals_against, 1.2)) / 3.0,
        _average(home.home_goal_diffs) / 3.0,
        -_average(away.away_goal_diffs) / 3.0,
    ]


def _outcome(home_goals: int, away_goals: int) -> int:
    return 0 if home_goals > away_goals else 2 if away_goals > home_goals else 1


def _update(states: dict[str, TeamState], match: MatchRecord):
    home = states.setdefault(match.home_team, TeamState())
    away = states.setdefault(match.away_team, TeamState())
    result = _outcome(match.home_goals, match.away_goals)
    home_points = 3 if result == 0 else 1 if result == 1 else 0
    away_points = 3 if result == 2 else 1 if result == 1 else 0

    expected_home = 1 / (1 + 10 ** ((away.elo - home.elo - 65) / 400))
    actual_home = 1 if result == 0 else 0.5 if result == 1 else 0
    change = 24 * (actual_home - expected_home)
    home.elo += change
    away.elo -= change

    home.recent_points.append(home_points)
    away.recent_points.append(away_points)
    home.recent_goals_for.append(match.home_goals)
    home.recent_goals_against.append(match.away_goals)
    away.recent_goals_for.append(match.away_goals)
    away.recent_goals_against.append(match.home_goals)
    goal_diff = match.home_goals - match.away_goals
    home.home_goal_diffs.append(goal_diff)
    away.away_goal_diffs.append(-goal_diff)


def build_examples(matches: list[MatchRecord]):
    states: dict[str, TeamState] = {}
    examples = []
    for match in sorted(matches, key=lambda item: item.date):
        home = states.setdefault(match.home_team, TeamState())
        away = states.setdefault(match.away_team, TeamState())
        examples.append((_features(home, away), _outcome(match.home_goals, match.away_goals)))
        _update(states, match)
    return examples, states


def _softmax(scores: list[float]) -> list[float]:
    maximum = max(scores)
    values = [math.exp(score - maximum) for score in scores]
    total = sum(values)
    return [value / total for value in values]


def probabilities(weights: list[list[float]], features: list[float]) -> list[float]:
    return _softmax([sum(weight * value for weight, value in zip(row, features)) for row in weights])


def fit(examples, epochs=350, learning_rate=0.08, seed=11):
    if not examples:
        raise ValueError("No hay partidos para entrenar.")
    weights = [[0.0 for _ in examples[0][0]] for _ in OUTCOMES]
    randomizer = random.Random(seed)
    indexes = list(range(len(examples)))
    class_counts = [sum(target == index for _, target in examples) for index in range(3)]
    class_weights = [math.sqrt(len(examples) / (3 * max(count, 1))) for count in class_counts]
    for _ in range(epochs):
        randomizer.shuffle(indexes)
        rate = learning_rate / (1 + _ * 0.006)
        for index in indexes:
            features, target = examples[index]
            predicted = probabilities(weights, features)
            for outcome_index, row in enumerate(weights):
                error = ((1.0 if target == outcome_index else 0.0) - predicted[outcome_index]) * class_weights[target]
                for feature_index, value in enumerate(features):
                    row[feature_index] += rate * error * value
    return weights


def evaluate(weights, examples):
    correct = 0
    log_loss = brier = 0.0
    matrix = [[0, 0, 0] for _ in OUTCOMES]
    for features, target in examples:
        predicted = probabilities(weights, features)
        guess = max(range(3), key=predicted.__getitem__)
        correct += guess == target
        matrix[target][guess] += 1
        log_loss -= math.log(max(predicted[target], 1e-15))
        brier += sum((predicted[index] - (1 if index == target else 0)) ** 2 for index in range(3))
    count = max(len(examples), 1)
    precision = []
    recall = []
    for index in range(3):
        true_positive = matrix[index][index]
        predicted_total = sum(matrix[actual][index] for actual in range(3))
        actual_total = sum(matrix[index])
        precision.append(round(true_positive / predicted_total, 4) if predicted_total else 0.0)
        recall.append(round(true_positive / actual_total, 4) if actual_total else 0.0)
    return {
        "matches": len(examples),
        "accuracy": round(correct / count, 4),
        "log_loss": round(log_loss / count, 4),
        "brier_score": round(brier / count, 4),
        "precision": dict(zip(OUTCOMES, precision)),
        "recall": dict(zip(OUTCOMES, recall)),
        "confusion_matrix": matrix,
    }


def train(matches: list[MatchRecord], test_ratio=0.2):
    examples, states = build_examples(matches)
    split = max(1, int(len(examples) * (1 - test_ratio)))
    weights = fit(examples[:split])
    return weights, states, evaluate(weights, examples[split:]), split


def parse_csv(text: str) -> list[MatchRecord]:
    records = []
    for row in csv.DictReader(text.splitlines()):
        home_team = row.get("HomeTeam") or row.get("Team 1")
        away_team = row.get("AwayTeam") or row.get("Team 2")
        home_goals = row.get("FTHG")
        away_goals = row.get("FTAG")
        if home_goals is None or away_goals is None:
            score = (row.get("FT") or "").split("-")
            if len(score) == 2:
                home_goals, away_goals = score
        if not all((row.get("Date"), home_team, away_team, home_goals, away_goals)):
            continue
        parsed_date = None
        for date_format in ("%d/%m/%Y", "%d/%m/%y", "%a %b %d %Y"):
            try:
                parsed_date = datetime.strptime(row["Date"], date_format)
                break
            except ValueError:
                pass
        if parsed_date:
            records.append(MatchRecord(parsed_date, home_team, away_team, int(home_goals), int(away_goals)))
    return records


def normalize_team_name(name: str) -> str:
    value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    value = re.sub(r"\b(fc|cf|afc|calcio|football club)\b", "", value)
    return re.sub(r"[^a-z0-9]", "", value)


def save_artifact(path: Path, league: str, weights, states, metrics, training_matches, split, data_through):
    payload = {
        "version": 1,
        "league": league,
        "algorithm": "multinomial logistic regression",
        "features": ["bias", "elo_difference", "recent_form", "recent_goals_for", "recent_goals_against", "home_form", "away_form"],
        "training_matches": training_matches,
        "chronological_split_index": split,
        "metrics": metrics,
        "weights": weights,
        "teams": {name: state.serializable() for name, state in states.items()},
        "data_through": data_through,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_artifact(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def predict_artifact(artifact: dict, home_team: str, away_team: str) -> dict:
    normalized = {normalize_team_name(name): (name, state) for name, state in artifact["teams"].items()}

    def baseline_state():
        states = list(artifact["teams"].values())
        fields = ("recent_points", "recent_goals_for", "recent_goals_against", "home_goal_diffs", "away_goal_diffs")
        return {
            "elo": _average([item["elo"] for item in states], 1500.0),
            **{field: [_average([_average(item[field]) for item in states], 0.0)] for field in fields},
        }

    def resolve(name):
        key = normalize_team_name(name)
        if key in normalized:
            return (*normalized[key], False)
        alias = TEAM_NAME_ALIASES.get(key)
        if alias in normalized:
            return (*normalized[alias], False)
        candidates = [value for candidate, value in normalized.items() if candidate in key or key in candidate]
        if len(candidates) == 1:
            return (*candidates[0], False)
        return name, baseline_state(), True

    home_name, home_raw, home_baseline = resolve(home_team)
    away_name, away_raw, away_baseline = resolve(away_team)

    def state(raw):
        item = TeamState(elo=raw["elo"])
        for field_name in ("recent_points", "recent_goals_for", "recent_goals_against", "home_goal_diffs", "away_goal_diffs"):
            getattr(item, field_name).extend(raw[field_name])
        return item

    values = probabilities(artifact["weights"], _features(state(home_raw), state(away_raw)))
    return {
        "home_team": home_name,
        "away_team": away_name,
        "home_win": round(values[0], 4),
        "draw": round(values[1], 4),
        "away_win": round(values[2], 4),
        "coverage": "partial" if home_baseline or away_baseline else "historical",
    }
