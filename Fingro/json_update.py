import json

def transform_data(original_data):
    transformed_data = {}
    for company, data in original_data.items():
        if data == "No annual report links found":
            transformed_data[company] = data
        else:
            company_data = {}
            for key, value in data.items():
                year = key.split("\n")[0].replace("Financial Year ", "").strip()
                source = "BSE" if "from bse" in key else "NSE"
                if year not in company_data:
                    company_data[year] = {}
                company_data[year][source] = value
            transformed_data[company] = company_data
    return transformed_data

# Read the original JSON data from the file
with open('annual_report_links.json', 'r') as file:
    original_data = json.load(file)

# Transform the data
transformed_data = transform_data(original_data)

# Write the transformed data to a new file
with open('dummy_links.json', 'w') as file:
    json.dump(transformed_data, file, indent=4)
