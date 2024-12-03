import pandas as pd
from bs4 import BeautifulSoup

with open('trading_economics_calendar_2024-12-03.html', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table', id='calendar')

data = []
for row in table.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

df = pd.DataFrame(data)

# Extract date from table header
date_str = soup.find('table', id='calendar').find('th').text.strip()

# Add date column to DataFrame
df['Date'] = date_str

print(df)
