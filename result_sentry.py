from playwright.sync_api import sync_playwright
import json
import time
import sys
import re

def clean_text(text):
    """Remove non-printable and non-ASCII characters."""
    return ''.join(c for c in text if c.isprintable()).strip()

def extract_score(text):
    """Extract and return only 'n - n' formatted score."""
    match = re.search(r'\d+\s*-\s*\d+', text)
    return match.group(0).strip() if match else ""


def scrape_team_results(team_name: str, league_hint: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.espn.com/soccer/schedule")

        page.get_by_role("button", name="Search").click()
        page.get_by_role("searchbox").fill(team_name)
        time.sleep(1.5)

        page.get_by_role("link", name=f'View all results for \'', exact=False).click()

        page.get_by_role("link", name="Teams").click()

        page.get_by_role("link", name=f"{team_name} {team_name} {league_hint}").click()
        page.wait_for_load_state("load")

        page.get_by_role("link", name="Results").click()
        page.wait_for_load_state("load")

        page.wait_for_selector('.ResponsiveTable.Table__results')

        results = []
        tables = page.locator('.ResponsiveTable.Table__results').all()

        for table in tables:
            rows = table.locator('tbody > tr').all()
            for row in rows:
                try:
                    date = row.locator('td:nth-child(1)').inner_text().strip()
                    competition = row.locator('td:nth-child(6)').inner_text().strip()
                    home_team = row.locator('td:nth-child(2)').inner_text().strip()
                    score = row.locator('td:nth-child(3)').inner_text().strip()
                    away_team = row.locator('td:nth-child(4)').inner_text().strip()

                    results.append({
                        "Date": clean_text(date),
                        "Home Team": clean_text(home_team),
                        "Visiting Team": clean_text(away_team),
                        "Score": extract_score(score),
                        "Competition": clean_text(competition)
                    })
                except Exception as e:
                    continue

        with open(f"{team_name}.json", "w") as f:
            json.dump(results, f, indent=2)

        browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python result_sentry.py <team_name> <league_hint>")
        sys.exit(1)

    team_name = sys.argv[1]
    league_hint = sys.argv[2]

    scrape_team_results(team_name, league_hint)
