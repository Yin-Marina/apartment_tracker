import requests
import re
import json
from datetime import datetime
import os
import subprocess
from bs4 import BeautifulSoup




# Get the current date
extraction_date = datetime.now().strftime('%Y-%m-%d')



# Define the path to the data file
minto_data_dir = './data/minto_data.json'

# Define minto URL
minto_url = "https://www.mintoapartments.com/ottawa/apartment-rentals/The-Carlisle/main.html#suites-rates"

def fetch_minto_data(url):



    try:
        # Send a GET request to the webpage
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the content of the webpage as text
            webpage_content = response.text
            # Extract data from each project apartment unit card
            unit_cards = BeautifulSoup(webpage_content, 'html.parser').find_all('div', class_='projects-apartamets-unit-card')

            # Initialize lists to store extracted data
            indexes = []
            suite_types = []
            suite_bathrooms = []
            suite_prices = []
            checkin_dates = []

            # Loop through each card and extract the relevant data
            for card in unit_cards:
                index = card.get('data-index')
                suite_type = card.get('data-bedrooms').strip('|')
                suite_bathroom = card.get('data-bathrooms').strip('|')
                suite_price = card.get('data-prices').strip('|').split('|')[0]  # Get the first price
                checkin_date = card.get('data-checkin').strip('|')
                
                indexes.append(index)
                suite_types.append(suite_type)
                suite_bathrooms.append(suite_bathroom)
                suite_prices.append(suite_price)
                checkin_dates.append(checkin_date)
            # Initialize an empty list for existing data
            existing_minto_data = []
    
            # Ensure the data directory exists
            os.makedirs(os.path.dirname(minto_data_dir), exist_ok=True)

            # Check if the data.json file exists and is not empty
            if os.path.exists(minto_data_dir) and os.path.getsize(minto_data_dir) > 0:
                try:
                    with open(minto_data_dir, 'r') as infile:
                        existing_minto_data = json.load(infile)
                except json.JSONDecodeError:
                    print("Error: data.json is not a valid JSON file.")
    
        # Check the date of the last entry
        last_entry_date = existing_minto_data[-1]['date_extracted'] if existing_minto_data else None
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
            existing_minto_data.extend(new_data)
        
            # Save the updated data to the JSON file
            with open(minto_data_dir, 'w') as outfile:
                json.dump(existing_minto_data, outfile, indent=4)
        
            print("New data extracted and appended successfully!")
        
        
        else:
            print("Data for today has already been extracted.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")



def fetch_data(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the content of the webpage as text
        webpage_content = response.text


        # Get the current date
        # extraction_date = datetime.now().strftime('%Y-%m-%d')

        # Initialize a list to hold the extracted data
        extracted_data = []

        location = BeautifulSoup(webpage_content, 'html.parser').find('input', {'name': 'form[building_id]'}).get('data-building-name')


        # Find all suite cards on the webpage (assuming they have a common class)
        suite_cards = BeautifulSoup(webpage_content, 'html.parser').find_all('div', class_='suite')  # Replace 'suite-card-class' with the actual class
        
        for card in suite_cards:
            # Extract the data for each suite
            unit_type = card.find('div', class_='suite-type').get_text(strip=True).replace('Unit Type', '')
            baths = card.find('div', class_='suite-bath').find('span', class_='value').get_text(strip=True)
            rent = card.find('div', class_='suite-rate').find('span', class_='value').get_text(strip=True)
            apt_number = card.find('div', class_='suite-numbers').find('span', class_='suite-number').get_text(strip=True)
            floor = card.find('div', class_='suite-floor').find('span', class_='suite-number').get_text(strip=True)
            date_text = card.find('div', class_='suite-availability').find('a').get_text(strip=True)

            # Combine the extracted data into a dictionary
            extracted_data.append({
                'apartment': location,
                'company': 'Fleming',
                'index': apt_number,
                'type': unit_type,
                'bathrooms': f'{baths} Bathroom(s)',
                'price': f'${rent} per month',
                'checkin_date': date_text,
                'date_extracted': extraction_date
            })

        # Print or save the extracted data (for demonstration purposes, printing it)
        print("fleming extracted data:")
        print(json.dumps(extracted_data, indent=4))
        
        # Save the extracted data to a JSON file
        data_file = './data/fleming_data.json'
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        with open(data_file, 'w') as outfile:
            json.dump(extracted_data, outfile, indent=4)
            return extracted_data
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    

# Define the path to the data file
fleming_data_dir = './data/fleming_data.json'

# Define fleming URL
fleming_urls = [
    "https://www.fpm.ca/residential/328-frank-st",
    "https://www.fpm.ca/residential/430-daly-ave",
    "https://www.fpm.ca/residential/387-daly-3",
    "https://www.fpm.ca/residential/195-cooper-st",
    "https://www.fpm.ca/residential/200-laurier-ave-east",
    "https://www.fpm.ca/residential/407-queen-st",
    "https://www.fpm.ca/residential/414-albert-st",
    "https://www.fpm.ca/residential/261-fifth-ave",
    "https://www.fpm.ca/residential/76-flora-st",
    "https://www.fpm.ca/residential/60-russell-ave"
]

def fetch_fleming_data(urls):


    extracted_data = []

    for url in urls:
        data = fetch_data(url)
        if data:
            extracted_data.append(data)
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(fleming_data_dir), exist_ok=True)

    # Check if the data.json file exists and is not empty
    if os.path.exists(fleming_data_dir) and os.path.getsize(fleming_data_dir) > 0:
        try:
            with open(fleming_data_dir, 'r') as infile:
                existing_fleming_data = json.load(infile)
        except json.JSONDecodeError:
            print("Error: data.json is not a valid JSON file.")
    
        # Check the date of the last entry
        last_entry_date = existing_fleming_data[-1]['date_extracted'] if existing_fleming_data else None
        last_entry_date = last_entry_date.split(" ")[0] if last_entry_date else None
    
        # Only add new data if the date is different
        if last_entry_date != extraction_date:
        
            # Append the new data to the existing data
            existing_fleming_data.extend(extracted_data)
        
            # Save the updated data to the JSON file
            with open(fleming_data_dir, 'w') as outfile:
                json.dump(existing_fleming_data, outfile, indent=4)
        
            print("New data extracted and appended successfully!")
        
        else:
            print("Data for today has already been extracted.")




















def main():
    fetch_minto_data(minto_url)

    fetch_fleming_data(fleming_urls)


if __name__ == "__main__":
    main()