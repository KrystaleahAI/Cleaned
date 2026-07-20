import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape
url = "http://www.rsdb.org/full"

# Send a request to the website
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table you want to scrape
# You need to update this selector based on the actual page structure
table = soup.find('table')

if table:
    # Extract data from the table
    data = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)  # Get rid of empty values

    # Write data to a CSV file
    with open('slurs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Column1', 'Column2', 'Column3'])  # Replace with your column headers
        for row in data:
            writer.writerow(row)
else:
    print("Table Not Found")