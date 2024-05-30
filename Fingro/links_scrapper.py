import requests
import pandas as pd
import io
from bs4 import BeautifulSoup
import pandas as pd
import json
nse_url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
# create Session from 'real' browser
headers = {
    'User-Agent': 'Mozilla/5.0'
}
s = requests.Session()
s.headers.update(headers)
url = 'https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv'
r = s.get(nse_url)
s.close()

# saving it to pd df for further preprocessing
df_nse = pd.read_csv(io.BytesIO(r.content))

def get_annual_report_links(stock_symbol):
    url = f'https://www.screener.in/company/{stock_symbol}/consolidated/#documents'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div_elements = soup.find_all('div', class_='documents annual-reports flex-column')
        for div_element in div_elements:
            ul_element = div_element.find('ul', class_='list-links')
            if ul_element:
                links = ul_element.find_all('a')
                links_dict = {}
                for link in links:
                    links_dict[link.text.strip()] = link['href']
                return {stock_symbol: links_dict}
    return {stock_symbol: 'No annual report links found'}
result = {}
for symbol in df_nse['SYMBOL']:
    links = get_annual_report_links(symbol)
    result.update(links)

# Convert the result to JSON format
json_data = json.dumps(result, indent=4)

# Save JSON data to a file
with open('annual_report_links.json', 'w') as file:
    file.write(json_data)

print('JSON data saved to annual_report_links.json')