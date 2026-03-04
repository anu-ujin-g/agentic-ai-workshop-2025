"""
Debug script to see what Google Places actually returns
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Geocode Times Square
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
geocode_params = {
    'address': 'Times Square, New York, NY',
    'key': os.getenv('GOOGLE_PLACES_API_KEY')
}

response = requests.get(geocode_url, params=geocode_params)
geocode_data = response.json()

if geocode_data['results']:
    location = geocode_data['results'][0]['geometry']['location']
    print(f"Location: {location}")

    # Search for restaurants
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    search_params = {
        'location': f"{location['lat']},{location['lng']}",
        'radius': 805,
        'type': 'restaurant',
        'key': os.getenv('GOOGLE_PLACES_API_KEY')
    }

    response = requests.get(search_url, params=search_params)
    places = response.json().get('results', [])

    print(f"\nFound {len(places)} restaurants\n")
    print("="*100)

    # Show first 5 with detailed info
    for i, place in enumerate(places[:5], 1):
        print(f"\n{i}. {place['name']}")
        print(f"   Types: {place.get('types', [])}")
        print(f"   Rating: {place.get('rating', 'N/A')}")
        print(f"   Price: {place.get('price_level', 'N/A')}")
        print(f"   Address: {place.get('vicinity', 'N/A')}")
