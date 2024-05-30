import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, urljoin, parse_qs
import requests

def extract_pdf_link(iframe_url):
    response = requests.get(iframe_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        iframe_tag = soup.find("iframe")
        if iframe_tag:
            pdf_src = iframe_tag["src"]
            parsed_url = urlparse(pdf_src)
            query_params = parse_qs(parsed_url.query)
            if "file" in query_params:
                pdf_link = query_params["file"][0]
                return pdf_link
    return None


url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListingLegal=yes&sid=1&ssid=3&smid=0"
max_pages = 2
data = []


chrome_options = Options()
chrome_options.add_argument("--headless")  


driver = webdriver.Chrome(options=chrome_options)


driver.get(url)


time.sleep(5)


for _ in range(max_pages):
    
    page_source = driver.page_source

    
    soup = BeautifulSoup(page_source, "html.parser")

   
    table = soup.find("table", {"id": "sample_1"})
    if table:
        rows = table.find_all("tr", {"role": "row"})
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2: 
                date = cells[0].get_text(strip=True)
                link = cells[1].find("a")["href"]
                title = cells[1].get_text(strip=True)
                
               
                if not link.startswith("http"):
                    link = urljoin(url, link)

            
                pdf_link = extract_pdf_link(link)

                if pdf_link:
                  
                    if not pdf_link.startswith("https://www.sebi.gov.in"):
                        pdf_link = urljoin("https://www.sebi.gov.in", pdf_link)
                    data.append({"date": date, "title": title, "link": pdf_link})

   
    driver.execute_script("searchFormNewsList('n');")
    time.sleep(5) 


driver.quit()


with open("extracted_links2.json", "w") as outfile:
    json.dump(data, outfile, indent=4)

print("Scraping complete. Extracted PDF links saved to extracted_links.json")
