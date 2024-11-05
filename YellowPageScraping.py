import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define a list to store all extracted data
my_list = []

# Extract function to fetch the HTML content
def extract(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_='v-card')

# Transform function to process HTML and extract specific data
def transform(nomanhtml):
    for item in nomanhtml:
        name = item.find('a', class_='business-name').text if item.find('a', class_='business-name') else ''
        address = item.find('div', class_='adr').text if item.find('div', class_='adr') else ''
        rating = item.find('a', class_='rating').text if item.find('a', class_='rating') else ''
        website = item.find('a', class_='track-visit-website')['href'] if item.find('a', class_='track-visit-website') else ''
        telephone = item.find('div', class_='phones phone primary').text if item.find('div', class_='phones phone primary') else ''
        year_in_business = item.find('div', class_='years-in-business').text if item.find('div', class_='years-in-business') else ''
        yp = item.find('div', class_='years-with-yp').text if item.find('div', class_='years-with-yp') else ''

        # Append all extracted data to a dictionary and then to my_list
        information = {
            'name': name,
            'address': address,
            'rating': rating,
            'website': website,
            'telephone': telephone,
            'year_in_business': year_in_business,
            'yp': yp
        }
        my_list.append(information)

# Load function to save the collected data into a CSV file
def load():
    df = pd.DataFrame(my_list)
    df.to_csv('yellow.csv', index=False)

# Main loop to iterate through the pages and extract data
for x in range(1, 22):
    print(f'Downloading page {x}')
    url = f'https://www.yellowpages.com/search?search_terms=dentist&geo_location_terms=New%20York%2C%20NY&page={x}'
    nomanhtml = extract(url)
    transform(nomanhtml)

# After data collection, save to CSV
print(f'Total records: {len(my_list)}')
load()
print('Data saved to yellow.csv')
