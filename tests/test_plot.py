import pandas as pd

from tennis_career import plot_career


def make_data():
    return pd.DataFrame(
        {
            "player": "Serena Williams",
            "result": ["W", "L", "W"],
            "player_age": [14.1, 20.5, 40.9],
            "age_diff": [-4.7, 0.0, 12.3],
        }
    )


def test_plot_career(tmp_path):
    output_path = tmp_path / "plot.png"
    fig = plot_career(make_data(), output_path)
    ax = fig.axes[0]
    assert ax.get_title() == "Serena Williams's Professional Matches, Age 14 to 40"
    assert len(ax.collections) == 2
    assert output_path.exists()
