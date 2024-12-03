import pandas as pd
from bs4 import BeautifulSoup

with open('trading_economics_calendar_2024-12-03.html', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table', id='calendar')

data = []
date_str = None
for element in table.find_all(['thead', 'tr']):
    if element.name == 'thead':
        date_str = element.find('th').text.strip()
    elif element.name == 'tr':
        cols = element.find_all('td')
        cols = [ele.text.strip().replace('Â', '').replace('\n', '').replace('â', '').replace('®', '') for ele in cols]
        row_data = [ele for ele in cols if ele]
        if date_str:
            row_data.insert(0, date_str)
        data.append(row_data)

df = pd.DataFrame(data[1:])
#df.columns = ['Date', 'Time', 'Country', 'Event', 'Actual', 'Previous', 'Consensus', 'Forecast']
print(df.dropna(subset=[4]).tail(50))
