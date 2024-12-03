import pandas as pd
from bs4 import BeautifulSoup

# Read the HTML file
with open('trading_economics_calendar_2024-12-03.html', 'r') as f:
    html_content = f.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Locate the table
table = soup.find('table', id='calendar')

data = []
date_str = None

# Extract data
for element in table.find_all(['thead', 'tr']):
    if element.name == 'thead':
        date_str = element.find('th').text.strip()
    elif element.name == 'tr':
        cols = element.find_all('td')
        # Clean and filter data
        cols = [ele.text.strip().replace('Â', '').replace('\n', '').replace('â', '').replace('®', '').replace('‚¬', '€') for ele in cols]
        row_data = [ele for ele in cols if ele]
        reference = element.find('span', class_='calendar-reference')
        if reference:
            row_data.append(reference.text.strip())
        else:
            row_data.append(None)
        if date_str:
            row_data.insert(0, date_str)
        data.append(row_data)

# Create DataFrame
df = pd.DataFrame(data[1:])
df.columns = ['Date', 'Time', 'Country', 'Event', 'Actual', 'Previous', 'Consensus', 'Forecast', 'Reference']

# Remove extra spaces from all values
df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
df = df.drop(columns=[2])
# Print the last 50 rows, filtering rows where column 4 (index 4) is not null
print(df.dropna(subset=[4]).head(50))
