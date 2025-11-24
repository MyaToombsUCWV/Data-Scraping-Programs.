import requests
import csv
from datetime import datetime, timedelta
import time

API_KEY = "AIzaSyCLSfXFk-EHlsR_qnQujczCIxntCJIeo7Q"
SEARCH_ENGINE_ID = "d352c226852134815"
QUERY = "NBA"

titles_found = []
links_found = []

# Function to generate monthly date ranges
def generate_monthly_ranges(start_date, end_date):
    ranges = []
    current = start_date
    while current < end_date:
        next_month = (current.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        if next_month > end_date:
            next_month = end_date
        ranges.append((current.strftime("%Y%m%d"), next_month.strftime("%Y%m%d")))
        current = next_month + timedelta(days=1)
    return ranges

# Set the date range
start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 1, 1)
date_ranges = generate_monthly_ranges(start_date, end_date)

# Loop through each monthly range
for start_str, end_str in date_ranges:
    start_index = 1
    while start_index <= 100:  # max 100 results per month
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"q=intitle:{QUERY}&cx={SEARCH_ENGINE_ID}&key={API_KEY}"
            f"&start={start_index}&sort=date:r:{start_str}:{end_str}"
        )
        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            break

        for item in data["items"]:
            title = item["title"]
            link = item["link"]
            if "NBA" in title.upper():
                titles_found.append(title)
                links_found.append(link)

        start_index += 10
        time.sleep(1)  # polite delay

# Save to CSV
with open("espn_nba_articles_2020_2025.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Link"])
    for t, l in zip(titles_found, links_found):
        writer.writerow([t, l])

print(f"Saved {len(titles_found)} articles to espn_nba_articles_2020_2025.csv")
