import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urljoin, parse_qs

# Function to extract direct PDF link from an iframe URL
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

# Load the JSON data containing iframe URLs
with open("scraped_Html_links.json", "r") as json_file:
    data = json.load(json_file)

# Base URL of the website
base_url = "https://www.sebi.gov.in"

# List to store extracted PDF links along with titles and dates
extracted_links = []

# Iterate through each item in the JSON data
for item in data:
    title = item["title"]
    date = item["date"]
    link = item["link"]

    # Check if link is a relative path, then prepend the base URL
    if not link.startswith("http"):
        link = urljoin(base_url, link)

    # Extract direct PDF link from the link (iframe URL)
    pdf_link = extract_pdf_link(link)

    if pdf_link:
        extracted_links.append({"title": title, "date": date, "link": pdf_link})

# Save the extracted links to a new JSON file
with open("extracted_links.json", "w") as output_file:
    json.dump(extracted_links, output_file, indent=4)

print("Extraction completed. Extracted links saved to 'extracted_links.json'.")
