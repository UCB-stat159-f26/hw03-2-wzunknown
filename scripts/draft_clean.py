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

rows = []
for m in matches:
    rows.append((m[0], m[4], m[16]))
df = pd.DataFrame(rows, columns=["date", "result", "opponent_dob"])

df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
df["opponent_dob"] = pd.to_datetime(
    df["opponent_dob"], format="%Y%m%d", errors="coerce"
)
df["player_age"] = (df["date"] - dob).dt.days / 365
df["opponent_age"] = (df["date"] - df["opponent_dob"]).dt.days / 365
df["age_diff"] = df["player_age"] - df["opponent_age"]

print(df.head())
print(len(df))
