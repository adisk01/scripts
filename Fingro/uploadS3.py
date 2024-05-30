import json

# Load the JSON data from the existing file
with open("extracted_links.json", "r") as json_file:
    data = json.load(json_file)

# Base URL of the website
base_url = "https://www.sebi.gov.in"

# Iterate through each item in the JSON data
for item in data:
    link = item["link"]

    # Check if link is a relative path, then prepend the base URL
    if not link.startswith("http"):
        item["link"] = base_url + link

# Save the modified JSON data to a new file
with open("modified_links.json", "w") as output_file:
    json.dump(data, output_file, indent=4)

print("Links modified and saved to 'modified_links.json'.")
