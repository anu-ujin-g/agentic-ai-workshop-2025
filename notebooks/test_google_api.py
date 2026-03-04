"""
Quick test to verify Google Places API is working
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_PLACES_API_KEY')

if not api_key:
    print("❌ GOOGLE_PLACES_API_KEY not found in .env file!")
    exit(1)

print(f"✅ API key found: {api_key[:20]}...")
print("\n🌐 Testing Google Places API...")

url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
params = {
    'query': 'restaurants in New York, NY',
    'type': 'restaurant',
    'key': api_key
}

try:
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    print(f"Status: {data['status']}")

    if data['status'] == 'OK':
        places = data.get('results', [])
        print(f"✅ API is working! Found {len(places)} restaurants")

        if places:
            print("\nFirst 3 results:")
            for i, place in enumerate(places[:3], 1):
                print(f"  {i}. {place['name']}")
                print(f"     Rating: {place.get('rating', 'N/A')}/5")
                print(f"     Address: {place.get('formatted_address', 'N/A')}")
        print("\n✅ Google Places API is working correctly!")
    else:
        print(f"❌ API Error: {data['status']}")
        if 'error_message' in data:
            print(f"   Message: {data['error_message']}")

except Exception as e:
    print(f"❌ Request failed: {e}")
