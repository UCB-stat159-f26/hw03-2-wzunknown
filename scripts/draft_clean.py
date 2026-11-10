# Draft: turn a career JS file into a data frame with ages.
import json
import re
import sys

import pandas as pd

player = sys.argv[1] if len(sys.argv) > 1 else "SerenaWilliams"

# matches
with open(f"data/{player}Career.js") as f:
    text = f.read()
text = text.replace("var morematchmx = ", "").strip().rstrip(";")
matches = json.loads(text)

# player date of birth
with open(f"data/{player}.js") as f:
    info = f.read()
dob = re.search(r"var dob=(\d+);", info).group(1)
dob = pd.to_datetime(dob, format="%Y%m%d")

DAYS_PER_YEAR = 365.25


def opponent_age(date, value):
    # female files give the opponent's date of birth, male files give the age
    if "." in value:
        return float(value)
    if len(value) == 8:
        return (date - pd.to_datetime(value, format="%Y%m%d")).days / DAYS_PER_YEAR
    return None


rows = []
for m in matches:
    date = pd.to_datetime(m[0], format="%Y%m%d")
    rows.append((date, m[4], opponent_age(date, m[16])))
df = pd.DataFrame(rows, columns=["date", "result", "opponent_age"])

df["player_age"] = (df["date"] - dob).dt.days / DAYS_PER_YEAR
df["age_diff"] = df["player_age"] - df["opponent_age"]
df = df.dropna()

print(df.head())
print(len(df))
