import requests
import re
import json
from datetime import datetime
import os

# Define the URL
url = "https://www.mintoapartments.com/ottawa/apartment-rentals/The-Carlisle/main.html#suites-rates"

# Define the path to the data file
data_file = './data/data.json'

# Ensure the data directory exists
os.makedirs(os.path.dirname(data_file), exist_ok=True)

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Extract the content of the webpage as text
    webpage_content = response.text
    
    # Updated regular expressions to match the new structure
    index_pattern = r'data-index="(\d+)"'
    suite_type_pattern = r'data-bedrooms="\|([\d\.]+)\|"'
    suite_bathrooms_pattern = r'data-bathrooms="\|([\d\.]+)\|"'
    suite_price_pattern = r'data-prices="\|(\d+)\|"'
    checkin_pattern = r'data-checkin="\|([\d\-]+)\|"'
    
    indexes = re.findall(index_pattern, webpage_content)
    suite_types = re.findall(suite_type_pattern, webpage_content)
    suite_bathrooms = re.findall(suite_bathrooms_pattern, webpage_content)
    suite_prices = re.findall(suite_price_pattern, webpage_content)
    checkin_dates = re.findall(checkin_pattern, webpage_content)
    
    # Get the current date
    extraction_date = datetime.now().strftime('%Y-%m-%d')
    
    # Initialize an empty list for existing data
    existing_data = []

    # Check if the data.json file exists and is not empty
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        try:
            with open(data_file, 'r') as infile:
                existing_data = json.load(infile)
        except json.JSONDecodeError:
            print("Error: data.json is not a valid JSON file.")
    
    # Check the date of the last entry
    last_entry_date = existing_data[-1]['date_extracted'] if existing_data else None
    last_entry_date = last_entry_date.split(" ")[0] if last_entry_date else None
    
    # Only add new data if the date is different
    if last_entry_date != extraction_date:
        new_data = []
        for idx, suite_type, suite_bathroom, suite_price, checkin_date in zip(indexes, suite_types, suite_bathrooms, suite_prices, checkin_dates):
            new_data.append({
                'apartment': 'Carlisle',
                'company': 'Minto',
                'index': idx,
                'type': f'{suite_type} Bedroom(s)',
                'bathrooms': f'{suite_bathroom} Bathroom(s)',
                'price': f'${suite_price} per month',
                'checkin_date': checkin_date,
                'date_extracted': extraction_date

            })
        
        # Append the new data to the existing data
        existing_data.extend(new_data)
        
        # Save the updated data to the JSON file
        with open(data_file, 'w') as outfile:
            json.dump(existing_data, outfile, indent=4)
        
        print("New data extracted and appended successfully!")
    else:
        print("Data for today has already been extracted.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
