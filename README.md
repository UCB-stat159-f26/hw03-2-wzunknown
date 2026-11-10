# tennis-career

Get and plot the career matches of a tennis player from [tennisabstract.com](https://www.tennisabstract.com).
The plot shows the player's age at each match and the age gap with the opponent, like the NYT graphic of Serena Williams's career.

## Install

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-wzunknown.git
```

## Usage

```python
from tennis_career import get_career_data, plot_career

# Serena Williams data and plot
serena = get_career_data("serena williams")
plot_career(serena)

# Rafael Nadal data and plot, saved to a file
rafa = get_career_data("Rafael Nadal")
plot_career(rafa, "nadal.png")

# raises ValueError: Player 'GastonSanchez' was not found on tennisabstract.com
unknown_player = get_career_data("GastonSanchez")
```

The player name can be written as `"serena williams"`, `"Serena Williams"`, or `"SerenaWilliams"`.

## Functions

- `get_career_data(player_name)` returns a data frame with one row per match:
  - `player`: the player's full name.
  - `date`: the date of the match.
  - `result`: `W` for a won match, `L` for a lost match.
  - `player_age`: the player's age at the match.
  - `opponent_age`: the opponent's age at the match.
  - `age_diff`: `player_age` minus `opponent_age`.
- `plot_career(data, output_path=None)` makes the scatter plot and returns the matplotlib figure.
  If `output_path` is given, the plot is also saved to that file.

## Data

For each player, two files are downloaded:

- `jsmatches/{Name}Career.js`: the career matches.
  Female files give the opponent's date of birth, and male files give the opponent's age.
- `jsmatches/{Name}.js`: the player info, with the player's full name and date of birth.

Matches without the opponent's age are dropped.

## Development

```bash
uv sync              # create the environment
uv run pytest        # run the tests
uv run ruff format   # format the code
uv run ruff check    # lint the code
```

The tests use the mock JS files in `tests/mock/` and fake downloads, so they never hit tennisabstract.com.
