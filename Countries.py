import time
from bs4 import BeautifulSoup
import requests
import csv

def get_countries():

    html = requests.get("https://www.theglobaleconomy.com/")

    # Parse the HTML of the webpage
    soup = BeautifulSoup(html.text, 'html.parser')

    # Find the select element
    select_element = soup.find('select')

    # Extract all the options in the select element
    options = select_element.find_all('option')

    # Print the values of all the options
    countries = [option.getText().replace(" ", "-").replace("(", "").replace(")", "") for option in options]

    return countries[1:]

countries = get_countries()

def countries_unbanked_dict(countries):

    country_dict = {}
    base_url = "https://www.theglobaleconomy.com/"

    for variable in countries:
        # Construct the full URL
        try:
            url = base_url + variable + "/percent_people_bank_accounts/"

            # Make a GET request to the URL
            response = requests.get(url)

            # Parse the HTML of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table')

            rows = table.find_all('tr')

            # Get the first row
            first_row = rows[1]

            # Extract the cells from the row
            cells = first_row.find_all('th')

            country_dict[variable] = cells[1].text
            time.sleep(1)
        except Exception as e:
            # Handle the error
            print("error: ",e," country:",variable)

    return country_dict

country_dict = countries_unbanked_dict(countries)


# Open a file for writing
with open('Un-banked bitcoin adoption/banked_dict.csv', 'w', newline='') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Write the column names
    writer.writerow(['key', 'value'])

    # Write the key-value pairs to the CSV file
    for key, value in country_dict.items():
        writer.writerow([key, value])

def crypto_adoption():

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    # Send a GET request to the URL
    response = requests.get("https://blog.chainalysis.com/reports/2022-global-crypto-adoption-index/",headers=headers)

    # Parse the HTML data
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table in the HTML
    table = soup.find('table')

    # Extract the data from the table
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    # Extract the first two columns from the data
    data = [row[:2] for row in data]

    # Print the resulting data
    my_dict = {row[0]: row[1] for row in data}

    return my_dict

adoption_dict = crypto_adoption()

with open('Un-banked bitcoin adoption/adoption_dict.csv', 'w', newline='') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Write the column names
    writer.writerow(['key', 'value'])

    # Write the key-value pairs to the CSV file
    for key, value in adoption_dict.items():
        writer.writerow([key, value])
