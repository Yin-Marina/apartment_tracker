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
        
            print("New minto data extracted and appended successfully!")
        
        
        else:
            print("Data for today has already been extracted.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# ----------------------------------------------------------------

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
            data_record = {
                'apartment': location.strip(),
                'company': 'Fleming',
                'index': apt_number.strip(),
                'type': unit_type.strip(),
                'bathrooms': f'{baths} Bathroom(s)',
                'price': f'{rent} per month',
                'checkin_date': date_text.strip(),
                'date_extracted': extraction_date.strip()
            }

            extracted_data.append(data_record)

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
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(fleming_data_dir), exist_ok=True)
    data_cache = []
    existing_fleming_data = []
    for url in urls:
        data = fetch_data(url)
        data_cache.extend(data)
    # Check if the data.json file exists and is not empty
    if os.path.exists(fleming_data_dir) and os.path.getsize(fleming_data_dir) > 0:
        try:
            with open(fleming_data_dir, 'r') as infile:
                existing_fleming_data = json.load(infile)
                # Append the new data to the existing data
                existing_fleming_data.extend(data_cache)
            with open(fleming_data_dir, 'w') as outfile:
                # Save the updated data to the JSON file
                json.dump(existing_fleming_data, outfile, indent=4)        
        except json.JSONDecodeError:
            print("Error: data.json is not a valid JSON file.")



# ----------------------------------------------------------------


jb_url = 'https://www.jbholdingsinc.ca/buyers/available-apartments'
# Define the path to the data file
jb_data_dir = './data/jb_data.json'

def fetch_jb_data(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the content of the webpage as text
            webpage_content = response.text
            # Extract data from each project apartment unit card
            unit_cards = BeautifulSoup(webpage_content, 'html.parser').find_all('div', class_=re.compile(r'\blisting-item\b'))

            # Initialize lists to store extracted data
            locations = []
            suite_types =[]
            links = []

            # Loop through each card and extract the relevant data
            for card in unit_cards:
                location = card.find('h3', class_='listing-address').text.strip()
                suite_type = [div.text.strip() for div in card.find_all('div', class_='listing-type')][0]
                link = card.find('a')['href']
                
                locations.append(location)
                suite_types.append(suite_type)
                links.append(link)

            # Initialize an empty list for existing data
            existing_jb_data = []
    
            # Ensure the data directory exists
            os.makedirs(os.path.dirname(jb_data_dir), exist_ok=True)

            # Check if the data.json file exists and is not empty
            if os.path.exists(jb_data_dir) and os.path.getsize(jb_data_dir) > 0:
                try:
                    with open(jb_data_dir, 'r') as infile:
                        existing_jb_data = json.load(infile)
                except json.JSONDecodeError:
                    print("Error: data.json is not a valid JSON file.")
    

            for location, suite_type, link in zip(locations, suite_types, links):
                new_data = {
                    'apartment': location,
                    'company': 'JBHoldings',
                    'type': f'{suite_type} Bedroom(s)',
                    'link' : f'https://www.jbholdingsinc.ca/{link}',
                    'date_extracted': extraction_date.strip()
                }
                print(new_data)

            # Append the new data to the existing data
            existing_jb_data.append(new_data)
        
            # Save the updated data to the JSON file
            with open(jb_data_dir, 'w') as outfile:
                json.dump(existing_jb_data, outfile, indent=4)
        
            print("New JB data extracted and appended successfully!")
        
        
        else:
            print("Data for today has already been extracted.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")       
        


def main():
    fetch_minto_data(minto_url)

    fetch_fleming_data(fleming_urls)

    fetch_jb_data(jb_url)


if __name__ == "__main__":
    main()