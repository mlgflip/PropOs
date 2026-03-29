import requests
import pandas as pd

API_KEY = "344ab32ff313473aa0188880b78162d3"

url = "https://api.rentcast.io/v1/listings/rental/long-term"

headers = {
    "X-Api-Key": API_KEY,
    "accept": "application/json"
}

zip_codes = ["33131", "33137", "33138", "33130", "33129", "33132", "33133", "33143"]

all_listings = []

for zip_code in zip_codes:
    params = {
        "zipCode": zip_code,
        "state": "FL",
        "limit": 50,
        "status": "Active"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    for listing in data:
        all_listings.append({
            "address": listing.get("formattedAddress"),
            "zip": listing.get("zipCode"),
            "price": listing.get("price"),
            "beds": listing.get("bedrooms"),
            "baths": listing.get("bathrooms"),
            "sqft": listing.get("squareFootage"),
            "year_built": listing.get("yearBuilt"),
            "property_type": listing.get("propertyType"),
            "latitude": listing.get("latitude"),
            "longitude": listing.get("longitude"),
        })
    print(f"Fetched {zip_code}")

df = pd.DataFrame(all_listings)
df.dropna(subset=["price", "sqft", "beds"], inplace=True)

df.to_csv("miami_rentals.csv", index=False)
print(f"Saved {len(df)} listings to miami_rentals.csv")
print(df.head())