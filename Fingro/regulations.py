import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Setup the Chrome driver with Selenium
# chrome_path = "/path/to/chromedriver"  # Update this with the path to your chromedriver executable
url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListingLegal=yes&sid=1&ssid=3&smid=0"
max_pages = 34  # Set the maximum number of pages to scrape
data = []

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode, without opening a browser window

# Initialize the Chrome driver
# driver_service = Service(chrome_path)
driver = webdriver.Chrome(options=chrome_options)

# Load the initial page
driver.get(url)

# Wait for some time to allow dynamic content to load (adjust the sleep time as needed)
time.sleep(5)

# Loop through pages
for _ in range(max_pages):
    # Extract the page source after dynamic content has loaded
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Extract information from the table rows
    table = soup.find("table", {"id": "sample_1"})
    if table:
        rows = table.find_all("tr", {"role": "row"})
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:  # Ensure there are at least two cells
                date = cells[0].get_text(strip=True)
                link = cells[1].find("a")["href"]
                title = cells[1].get_text(strip=True)
                data.append({"date": date, "title": title, "link": link})

    # Simulate clicking on the next page button using JavaScript
    driver.execute_script("searchFormNewsList('n');")
    time.sleep(5)  # Wait for the next page to load

# Close the driver
driver.quit()

# Save the data to a JSON file
with open("scraped_Html_links.json", "w") as outfile:
    json.dump(data, outfile, indent=4)

print("Scraping complete. Data saved to scraped_data.json")