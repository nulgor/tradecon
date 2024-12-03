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
        row_data = [ele if ele else None for ele in cols]  # Replace empty values with None
        
        # Extract the calendar-event and calendar-reference
        event_col = element.find('a', class_='calendar-event')
        reference_col = element.find('span', class_='calendar-reference')
        
        # Add event and reference text to row_data
        if event_col:
            event_text = event_col.get_text(strip=True)
        else:
            event_text = cols[2].text.strip()
        reference_text = reference_col.get_text(strip=True) if reference_col else None  # Use None if reference_text is empty
        
        # Insert the date and add event and reference text
        row_data.insert(0, date_str)  # Insert date at the beginning if needed
        row_data.append(event_text)  # Add event text
        row_data.append(reference_text)  # Add reference text
        
        data.append(row_data)

# Create DataFrame
df = pd.DataFrame(data[1:])

# Remove extra spaces from all values
df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)


# Drop the column if it's not required
df = df.dropna(subset=[4])
df = df.drop(columns=[2,3,5])  # Adjust if necessary

# Print the last 50 rows, filtering rows where column 4 (index 4) is not null
print(df.tail(50))
print(df.iloc[0])
