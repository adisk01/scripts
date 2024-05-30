from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json


chrome_options = Options()
chrome_options.add_argument('--headless')  

driver = webdriver.Chrome(options=chrome_options)


url = 'https://www.bankbazaar.com/gold-rate-india.html'

driver.get(url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table = soup.find('table', class_='ui darker blue celled striped center aligned table mt-z mb-z')
if table:
    gold_prices = {}
    rows = table.find_all('tr')[1:]

    for row in rows:
        columns = row.find_all('td')
        city = columns[0].find('a').text
        price_22_carat = columns[1].text.strip()
        price_24_carat = columns[2].text.strip()


        gold_prices[city] = {
            '22 carat': price_22_carat,
            '24 carat': price_24_carat
        }

    json_output = json.dumps(gold_prices, indent=4)

    with open('gold_prices.json', 'w') as json_file:
        json_file.write(json_output)

    print('Data saved to gold_prices.json')
else:
    print('Table not found on the webpage.')

driver.quit()
