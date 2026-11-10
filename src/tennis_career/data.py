import json
import re
import urllib.error
import urllib.request

import pandas as pd

BASE_URL = "https://www.tennisabstract.com/jsmatches"
DAYS_PER_YEAR = 365.25

# column positions in the career JS file
DATE_COL = 0
RESULT_COL = 4
OPPONENT_COL = 16


def get_career_data(player_name: str) -> pd.DataFrame:
    """Get the career matches of a player as a clean data frame."""
    name = _to_name_param(player_name)
    try:
        career_js = _fetch_text(f"{BASE_URL}/{name}Career.js")
    except urllib.error.HTTPError as err:
        if err.code == 404:
            raise ValueError(
                f"Player '{player_name}' was not found on tennisabstract.com"
            ) from err
        raise
    player_js = _fetch_text(f"{BASE_URL}/{name}.js")
    data = _clean_matches(_parse_matches(career_js), _parse_dob(player_js))
    data.insert(0, "player", _parse_full_name(player_js))
    return data


def _to_name_param(player_name: str) -> str:
    """Turn 'serena williams' into 'SerenaWilliams'."""
    words = player_name.split()
    return "".join(word[0].upper() + word[1:] for word in words)


def _fetch_text(url: str) -> str:
    """Download a web page as text."""
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def _parse_matches(career_js: str) -> list:
    """Read the list of matches from a career JS file."""
    text = career_js.replace("var morematchmx = ", "").strip().rstrip(";")
    return json.loads(text)


def _parse_dob(player_js: str) -> pd.Timestamp:
    """Read the player's date of birth from the player JS file."""
    dob = re.search(r"var dob\s*=\s*(\d{8})", player_js).group(1)
    return pd.to_datetime(dob, format="%Y%m%d")


def _parse_full_name(player_js: str) -> str:
    """Read the player's full name from the player JS file."""
    return re.search(r"var fullname\s*=\s*'([^']*)'", player_js).group(1)


def _years_between(start: pd.Timestamp, end: pd.Timestamp) -> float:
    """Number of years between two dates."""
    return (end - start).days / DAYS_PER_YEAR


def _opponent_age(match_date: pd.Timestamp, opponent_value: str) -> float:
    """Opponent age from a birth date (female) or an age (male)."""
    if len(opponent_value) == 8 and opponent_value.isdigit():
        dob = pd.to_datetime(opponent_value, format="%Y%m%d")
        return _years_between(dob, match_date)
    if opponent_value:
        return float(opponent_value)
    return float("nan")


def _clean_matches(matches: list, player_dob: pd.Timestamp) -> pd.DataFrame:
    """Build a data frame with the player's age and the age gap of each match."""
    dates = pd.to_datetime([match[DATE_COL] for match in matches], format="%Y%m%d")
    data = pd.DataFrame({"date": dates})
    data["result"] = [match[RESULT_COL] for match in matches]
    data["player_age"] = [_years_between(player_dob, date) for date in dates]
    data["opponent_age"] = [
        _opponent_age(date, match[OPPONENT_COL]) for date, match in zip(dates, matches)
    ]
    data["age_diff"] = data["player_age"] - data["opponent_age"]
    return data.dropna().reset_index(drop=True)
