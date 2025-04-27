# ResultSentry

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

ResultSentry is a Python-based web scraper that fetches soccer match results for a specific team from ESPN's website and saves the data into a clean, structured `<team_name>.json` file.

## Features

- Scrapes:
  - Date
  - Home Team
  - Visiting Team
  - Final Score (n - n format only)
  - Competition
- Cleans text to remove hidden special characters
- Saves the output into an easy-to-use JSON file

## Requirements

- Python 3.8 or higher
- The following Python libraries must be installes manually
  - playwright

Install manually:

```bash
pip install playwright
python -m playwright instal
```

## How to Use

1. Clone or download the repository

```bash
git clone https://github.com/KOrtizLedezma/ResultSentry.git
cd ResultSentry
```

2. Install dependencies manually

```bash
pip install playwright
python -m playwright install
```

3. Run the scrapper:

```bash
python result_sentry.py "Team Name" "League Name"
```

Examples

```bash
python result_sentry.py "Barcelona" "LALIGA"
python result_sentry.py "Manchester United" "Premier League"
```

4. Notes

- The scraper targets the current season's results only.
- The score field is automatically cleaned to follow a `n - n` format.
- Non-printable characters are automatically removed from the output.

