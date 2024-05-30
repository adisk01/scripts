import os
import requests
import shutil
import zipfile
import json
from urllib.parse import urlparse, unquote

base_folder = os.path.join(os.path.expanduser("~"), "Desktop", "annual_reports")
os.makedirs(base_folder, exist_ok=True)

# Load data from the JSON file
json_file_path = "./dummy_links.json"  
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

for company, reports in data.items():
    if isinstance(reports, str) and reports == "No annual report links found":
        print(f"No annual report links found for {company}")
        continue
    company_folder = os.path.join(base_folder, company)
    os.makedirs(company_folder, exist_ok=True) 

    for year, url_dict in reports.items():
        for exchange, file_url in url_dict.items():
            try:
                parsed_url = urlparse(file_url)
            except Exception as e:
                print(f"Error parsing URL for {company} ({year}): {e}")
                continue
            
            file_name = unquote(os.path.basename(parsed_url.path))

            # Handle special case for ZIP files
            if file_name.endswith('.zip'):
                zip_file_path = os.path.join(company_folder, f"{year}_{exchange}.zip")
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(file_url, headers=headers, stream=True)
                with open(zip_file_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)
                del response

                # Extract PDF files from the ZIP archive
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    for item in zip_ref.namelist():
                        if item.lower().endswith('.pdf'):
                            pdf_file_name = f"{year}_{exchange}.pdf"
                            zip_ref.extract(item, path=company_folder)
                            os.rename(os.path.join(company_folder, item), os.path.join(company_folder, pdf_file_name))
                            print(f"Downloaded and renamed {pdf_file_name} for {company} ({year})")

                # Remove the ZIP file after extraction
                os.remove(zip_file_path)
            else:
                # Rename the file with the year and exchange and save it to the company folder
                renamed_file = f"{year}_{exchange}.pdf"
                file_path = os.path.join(company_folder, renamed_file)

                # Download the file (PDF)
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(file_url, headers=headers, stream=True)
                with open(file_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)
                del response

                print(f"Downloaded {renamed_file} for {company} ({year})")

print("All files downloaded and renamed successfully.")
