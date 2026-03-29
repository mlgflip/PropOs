import requests
import pandas as pd

API_KEY = "344ab32ff313473aa0188880b78162d3"  # paste your key

url = "https://api.rentcast.io/v1/listings/rental/long-term"

params = {
    "city": "Miami",
    "state": "FL",
    "limit": 50,
    "status": "Active"
}

headers = {
    "X-Api-Key": API_KEY,
    "accept": "application/json"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# pull out the fields you care about
listings = []
for listing in data:
    listings.append({
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

df = pd.DataFrame(listings)
df.dropna(subset=["price", "sqft", "beds"], inplace=True)  # drop rows missing key fields

df.to_csv("miami_rentals.csv", index=False)
print(f"Saved {len(df)} listings to miami_rentals.csv")
print(df.head())