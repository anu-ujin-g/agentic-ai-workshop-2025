"""
Quick diagnostic to check which APIs are working
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_PLACES_API_KEY')

if not api_key:
    print("❌ No API key found in .env file!")
    exit(1)

print(f"API Key: {api_key[:20]}...\n")
print("="*70)

# Test 1: Geocoding API
print("\n1️⃣  Testing Geocoding API...")
print("   URL: https://maps.googleapis.com/maps/api/geocode/json")

geocode_response = requests.get(
    'https://maps.googleapis.com/maps/api/geocode/json',
    params={
        'address': 'Times Square, New York',
        'key': api_key
    }
)
geocode_data = geocode_response.json()

print(f"   Status: {geocode_data['status']}")

if geocode_data['status'] == 'OK':
    print(f"   ✅ Geocoding API WORKS!")
    print(f"   Found: {geocode_data['results'][0]['formatted_address']}")
    lat_lng = geocode_data['results'][0]['geometry']['location']
    print(f"   Coordinates: {lat_lng['lat']}, {lat_lng['lng']}")
elif geocode_data['status'] == 'REQUEST_DENIED':
    print(f"   ❌ Geocoding API NOT ENABLED or API key not authorized")
    if 'error_message' in geocode_data:
        print(f"   Error: {geocode_data['error_message']}")
else:
    print(f"   ❌ Error: {geocode_data['status']}")
    if 'error_message' in geocode_data:
        print(f"   Message: {geocode_data['error_message']}")

print("\n" + "="*70)

# Test 2: Places API
print("\n2️⃣  Testing Places API (Nearby Search)...")
print("   URL: https://maps.googleapis.com/maps/api/place/nearbysearch/json")

places_response = requests.get(
    'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
    params={
        'location': '40.758896,-73.985130',  # Times Square
        'radius': 805,
        'type': 'restaurant',
        'key': api_key
    }
)
places_data = places_response.json()

print(f"   Status: {places_data['status']}")

if places_data['status'] == 'OK':
    print(f"   ✅ Places API WORKS!")
    print(f"   Found: {len(places_data.get('results', []))} restaurants")
elif places_data['status'] == 'REQUEST_DENIED':
    print(f"   ❌ Places API NOT ENABLED or API key not authorized")
    if 'error_message' in places_data:
        print(f"   Error: {places_data['error_message']}")
else:
    print(f"   ❌ Error: {places_data['status']}")
    if 'error_message' in places_data:
        print(f"   Message: {places_data['error_message']}")

print("\n" + "="*70)
print("\n📋 SUMMARY\n")

geocoding_works = geocode_data['status'] == 'OK'
places_works = places_data['status'] == 'OK'

if geocoding_works and places_works:
    print("✅ Both APIs working! You're ready to use mATEre d'")
elif geocoding_works and not places_works:
    print("⚠️  Geocoding works, but Places API needs fixing")
    print("   Action: Enable Places API in Google Cloud Console")
elif not geocoding_works and places_works:
    print("⚠️  Places works, but Geocoding API needs fixing")
    print("   Action: Enable Geocoding API in Google Cloud Console")
else:
    print("❌ Neither API working!")
    print("\n🔧 SOLUTIONS:")
    print("\n   Option 1: Wait 2-5 minutes (APIs take time to activate)")
    print("   Option 2: Create a NEW API key:")
    print("      1. Go to: https://console.cloud.google.com/apis/credentials")
    print("      2. Delete old API key")
    print("      3. Click '+ CREATE CREDENTIALS' → 'API key'")
    print("      4. Copy new key")
    print("      5. Update .env file with new key")
    print("      6. Wait 1-2 minutes")
    print("      7. Run this script again")
    print("\n   Option 3: Check both APIs are enabled:")
    print("      Go to: https://console.cloud.google.com/apis/dashboard")
    print("      You should see:")
    print("        ✓ Geocoding API")
    print("        ✓ Places API")

print("\n" + "="*70)
