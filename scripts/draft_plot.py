# Draft: scatter plot of a player's career, based on the HW2 plot.
import sys

import matplotlib.pyplot as plt
import pandas as pd

player = sys.argv[1] if len(sys.argv) > 1 else "SerenaWilliams"
df = pd.read_csv(f"data/{player}.csv")

COLORS = {"W": "#4acbed", "L": "#953a8c"}
LABELS = {"W": "Match won", "L": "Match lost"}

fig, ax = plt.subplots(figsize=(10, 7))
ax.axhline(0, color="gray", linewidth=1, zorder=1)
ax.grid(color="#e6e6e6", linewidth=0.8)

for result in ["W", "L"]:
    g = df[df["result"] == result]
    ax.scatter(
        g["player_age"],
        g["age_diff"],
        color=COLORS[result],
        label=LABELS[result],
        s=28,
        alpha=0.8,
        edgecolors="none",
        zorder=2,
    )

ax.set_xticks(range(14, 41, 2))
ax.set_yticks([-20, -10, 0, 10, 20])
ax.set_yticklabels(["-20", "-10", "Same age", "+10", "+20 years"])
ax.xaxis.set_ticks_position("top")
for side in ax.spines.values():
    side.set_visible(False)
ax.tick_params(length=0, colors="gray")

name = df["player"][0]
first_age = int(df["player_age"].min())
last_age = int(df["player_age"].max())
ax.set_title(
    f"{name}'s Professional Matches, Age {first_age} to {last_age}",
    fontweight="bold",
    fontsize=14,
    pad=42,
)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.10), ncol=2, frameon=False)

fig.savefig(f"data/{player}.png", dpi=150)
