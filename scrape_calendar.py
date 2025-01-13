import pandas as pd
from bs4 import BeautifulSoup
import os

# Define paths
data_folder = 'data'  # Path to the folder containing HTML files
output_file = 'calendar_data.xlsx'  # Path to the Excel file

# Function to parse an HTML file and extract the DataFrame
def parse_html_to_df(html_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', id='calendar')

    data = []
    date_str = None

    # Extract data
    for element in table.find_all(['thead', 'tr']):
        if element.name == 'thead':
            date_str = element.find('th').text.strip()
        elif element.name == 'tr':
            cols = element.find_all('td')
            cols = [ele.text.strip().replace('Â', '').replace('\n', '').replace('â', '').replace('®', '').replace('‚¬', '€') for ele in cols]
            row_data = [ele if ele else None for ele in cols]

            event_col = element.find('a', class_='calendar-event')
            reference_col = element.find('span', class_='calendar-reference')

            event_text = event_col.get_text(strip=True) if event_col else None
            reference_text = reference_col.get_text(strip=True) if reference_col else None

            row_data.insert(0, date_str)  # Insert date at the beginning
            row_data.append(event_text)  # Add event text
            row_data.append(reference_text)  # Add reference text

            data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data[1:])
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df[12] = df.apply(lambda row: row[5] if pd.isna(row[12]) else row[12], axis=1)
    df = df.drop(columns=[2, 3, 5, 10, 11])  # Adjust if necessary
    df.columns = ['Date', 'Time', 'Country', 'Actual', 'Previous', 'Consensus', 'Forecast', 'Event', 'Reference']
    df = df[['Date', 'Time', 'Country', 'Event', 'Reference', 'Actual', 'Previous', 'Consensus', 'Forecast']]

    # Remove rows where the 'Country' column is empty
    df = df.dropna(subset=['Country'])

    # Separate 'Day' and 'Date'
    df[['Day', 'Date']] = df['Date'].str.extract(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+(.*)$')
    
    # Convert 'Date' to the format '%Y-%m-%d'
    df['Date'] = pd.to_datetime(df['Date'], format='%B %d %Y').dt.strftime('%Y-%m-%d')

    # Rearrange columns
    df = df[['Day', 'Date', 'Time', 'Country', 'Event', 'Reference', 'Actual', 'Previous', 'Consensus', 'Forecast']]

    return df

# Accumulate all DataFrames in memory
all_data = []

# Iterate through HTML files in the folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.html'):
        html_path = os.path.join(data_folder, file_name)
        new_df = parse_html_to_df(html_path)
        all_data.append(new_df)
        print(f"Processed {file_name}")

# Combine all DataFrames
combined_df = pd.concat(all_data, ignore_index=True)

# Read existing data from the Excel file if it exists
if os.path.exists(output_file):
    existing_df = pd.read_excel(output_file)
    combined_df = pd.concat([existing_df, combined_df])

# Drop duplicates based on key columns
combined_df.drop_duplicates(subset=['Date', 'Time', 'Event'], inplace=True)

# Save to Excel
with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
    combined_df.to_excel(writer, index=False)

print("Data processing and saving completed.")
