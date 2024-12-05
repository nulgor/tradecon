


playwright install# Trading Economics Calendar Scraper

This project scrapes data from the Trading Economics calendar and saves it to an Excel file.

## Requirements

- Python 3.7+
- Playwright
- BeautifulSoup4
- pandas
- openpyxl

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/trading-economics-scraper.git
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run `scrape_calendar.py` to scrape the calendar data and save it to `calendar_data.xlsx`.
2. Run `main.py` to scrape the calendar data and save it to `data/trading_economics_calendar_{date}.html`.

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

## Disclaimer

This project is for educational purposes only. The author is not responsible for any misuse of the scraper.
