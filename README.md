


# Calendar Scraper

This project scrapes data from the Trading Economics calendar and saves it to an Excel file.

## Requirements

- Python 3.7+
- Playwright
- BeautifulSoup4
- pandas
- openpyxl

## Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Playwright:
   ```bash
   playwright install
   ```

## Usage

1. Run `download_data.py` to download the calendar data as HTML files.
2. Run `scrape_calendar.py` to scrape the calendar data and save it to `calendar_data.xlsx`.


## Data

The scraped data is saved in `calendar_data.xlsx` and includes the following columns:

- Day
- Date
- Time
- Country
- Event
- Reference
- Actual
- Previous
- Consensus
- Forecast

## Notes

- The scraper uses Playwright to automate the browser interaction and BeautifulSoup to parse the HTML.
- The scraper saves the data to an Excel file using pandas.
- The scraper can be configured to scrape data for a specific date range.
- The scraper can be configured to run headless (without a GUI).


