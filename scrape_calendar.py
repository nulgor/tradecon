import requests
from bs4 import BeautifulSoup

def scrape_trading_economics_calendar(html_content):
    """
    Scrapes the economic calendar data from the given HTML content.

    Args:
        html_content: The HTML content of the Trading Economics calendar page.

    Returns:
        A list of dictionaries, where each dictionary represents a row in the table 
        and contains the scraped data.  Returns an empty list if no table is found.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'calendar'})

    if table is None:
        return []

    rows = []
    for row in table.find_all('tr'):
        cols = row.find_all(['td', 'th'])  # Handle both <td> and <th> tags
        row_data = {}
        if cols: #Skip empty rows
            if cols[0].has_attr('colspan'): #Handle header rows with colspan
                row_data['date'] = cols[0].text.strip()
            else:
                try:
                    row_data['time'] = cols[0].span.text.strip()
                    row_data['country'] = cols[1].find('div', class_='flag')['title']
                    row_data['iso'] = cols[1].find('td', class_='calendar-iso').text.strip()
                    row_data['event'] = cols[2].a.text.strip()
                    row_data['actual'] = cols[3].span.text.strip() if cols[3].span else cols[3].text.strip()
                    row_data['previous'] = cols[4].span.text.strip() if cols[4].span else cols[4].text.strip()
                    row_data['consensus'] = cols[5].a.text.strip() if cols[5].a else cols[5].text.strip()
                    row_data['forecast'] = cols[6].a.text.strip() if cols[6].a else cols[6].text.strip()
                    rows.append(row_data)
                except (AttributeError, IndexError) as e:
                    #Handle cases where data might be missing in a row.  
                    #In a production scraper, log the error and the row for debugging.
                    pass

    return rows


# Example usage (replace with your actual file reading):
with open('trading_economics_calendar_2024-12-03.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

calendar_data = scrape_trading_economics_calendar(html_content)

for row in calendar_
    print(row)

