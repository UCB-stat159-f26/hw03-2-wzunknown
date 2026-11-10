import math

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

COLORS = {"W": "#4acbed", "L": "#953a8c"}
LABELS = {"W": "Match won", "L": "Match lost"}
POINT_STYLE = {"s": 28, "alpha": 0.8, "edgecolors": "none", "zorder": 2}
Y_TICKS = [-20, -10, 0, 10, 20]
Y_LABELS = ["-20", "-10", "Same age", "+10", "+20 years"]


def plot_career(data: pd.DataFrame, output_path: str | None = None):
    """Plot the player's age vs. the age gap with each opponent."""
    fig, ax = plt.subplots(figsize=(10, 7))
    _draw_points(ax, data)
    _style_axes(ax)
    _add_title(ax, data)
    if output_path is not None:
        fig.savefig(output_path, dpi=150)
    return fig


def _draw_points(ax, data: pd.DataFrame):
    """Draw won and lost matches in two colors."""
    for result in ["W", "L"]:
        matches = data[data["result"] == result]
        ax.scatter(
            matches["player_age"],
            matches["age_diff"],
            color=COLORS[result],
            label=LABELS[result],
            **POINT_STYLE,
        )


def _style_axes(ax):
    """Style the axes like the NYT graphic."""
    ax.axhline(0, color="gray", linewidth=1, zorder=1)
    ax.grid(color="#e6e6e6", linewidth=0.8)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.xaxis.set_ticks_position("top")
    ax.set_yticks(Y_TICKS, Y_LABELS)
    ax.tick_params(length=0, colors="gray")
    for spine in ax.spines.values():
        spine.set_visible(False)


def _add_title(ax, data: pd.DataFrame):
    """Add the title and the legend."""
    player = data["player"].iloc[0]
    first_age = math.floor(data["player_age"].min())
    last_age = math.floor(data["player_age"].max())
    title = f"{player}'s Professional Matches, Age {first_age} to {last_age}"
    ax.set_title(title, fontweight="bold", fontsize=14, pad=42)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.10), ncol=2, frameon=False)
