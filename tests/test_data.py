import math
import urllib.error
from pathlib import Path

import pandas as pd
import pytest

from tennis_career import data

MOCK_DIR = Path(__file__).parent / "mock"
FEMALE_JS = (MOCK_DIR / "FemalePlayerCareer.js").read_text()
MALE_JS = (MOCK_DIR / "MalePlayerCareer.js").read_text()
PLAYER_JS = "var fullname = 'Serena Williams';\nvar dob=19810926;\n"


def test_to_name_param():
    assert data._to_name_param("serena williams") == "SerenaWilliams"
    assert data._to_name_param("Serena Williams") == "SerenaWilliams"
    assert data._to_name_param("SerenaWilliams") == "SerenaWilliams"


def test_parse_matches():
    assert len(data._parse_matches(FEMALE_JS)) == 3
    assert len(data._parse_matches(MALE_JS)) == 3
    assert data._parse_matches(FEMALE_JS)[0][11] == "Anne Miller"


def test_parse_player_js():
    assert data._parse_dob(PLAYER_JS) == pd.Timestamp("1981-09-26")
    assert data._parse_full_name(PLAYER_JS) == "Serena Williams"


def test_opponent_age():
    match_date = pd.Timestamp("1995-10-30")
    assert data._opponent_age(match_date, "19770119") == pytest.approx(18.776, abs=1e-3)
    assert data._opponent_age(match_date, "22.264202601") == 22.264202601
    assert data._opponent_age(match_date, "22") == 22
    assert math.isnan(data._opponent_age(match_date, ""))


def test_clean_matches_female():
    matches = data._parse_matches(FEMALE_JS)
    df = data._clean_matches(matches, pd.Timestamp("1981-09-26"))
    assert list(df["result"]) == ["L", "L", "L"]
    assert df["player_age"][0] == pytest.approx(14.092, abs=1e-3)
    assert df["age_diff"][0] == pytest.approx(14.092 - 18.776, abs=1e-3)


def test_clean_matches_male():
    matches = data._parse_matches(MALE_JS)
    df = data._clean_matches(matches, pd.Timestamp("1986-06-03"))
    assert list(df["result"]) == ["L", "L", "W"]
    assert df["opponent_age"][0] == 22.264202601


def fake_fetch(url):
    return FEMALE_JS if url.endswith("Career.js") else PLAYER_JS


def fake_fetch_error(code):
    def fetch(url):
        raise urllib.error.HTTPError(url, code, "error", None, None)

    return fetch


def test_get_career_data(monkeypatch):
    monkeypatch.setattr(data, "_fetch_text", fake_fetch)
    df = data.get_career_data("serena williams")
    assert len(df) == 3
    assert df["player"][0] == "Serena Williams"


def test_get_career_data_unknown_player(monkeypatch):
    monkeypatch.setattr(data, "_fetch_text", fake_fetch_error(404))
    with pytest.raises(ValueError, match="not found"):
        data.get_career_data("Gaston Sanchez")


def test_get_career_data_other_error(monkeypatch):
    monkeypatch.setattr(data, "_fetch_text", fake_fetch_error(403))
    with pytest.raises(urllib.error.HTTPError):
        data.get_career_data("Serena Williams")
