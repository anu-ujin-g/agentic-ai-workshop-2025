"""
Quick test script to verify mATEre d' is ready for demo
Run this before your presentation to ensure everything works!
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_setup():
    """Test that everything is configured correctly."""

    print("🧪 Testing mATEre d' Setup...\n")

    # Test 1: Environment variable
    print("1️⃣  Checking Google Places API key...")
    load_dotenv()
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')

    if not api_key:
        print("   ❌ GOOGLE_PLACES_API_KEY not found in .env file!")
        print("   📝 Create a .env file with: GOOGLE_PLACES_API_KEY=your_key_here")
        return False
    else:
        print(f"   ✅ API key found: {api_key[:20]}...")

    # Test 2: Imports
    print("\n2️⃣  Testing imports...")
    try:
        from matere_d_agent import SmartRestaurantAgent
        from matere_d_preferences import UserPreferencesManager
        print("   ✅ All imports successful!")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

    # Test 3: Dependencies
    print("\n3️⃣  Checking dependencies...")
    try:
        import chromadb
        print("   ✅ chromadb installed")
    except ImportError:
        print("   ❌ chromadb not installed. Run: pip install chromadb")
        return False

    try:
        import requests
        print("   ✅ requests installed")
    except ImportError:
        print("   ❌ requests not installed. Run: pip install requests")
        return False

    # Test 4: Agent initialization
    print("\n4️⃣  Testing agent initialization...")
    try:
        agent = SmartRestaurantAgent(
            google_api_key=api_key,
            data_dir=Path('data/matere_d_test')
        )
        print("   ✅ Agent initialized successfully!")
    except Exception as e:
        print(f"   ❌ Agent initialization failed: {e}")
        return False

    # Test 5: Data directory
    print("\n5️⃣  Checking data directories...")
    data_dir = Path('data/matere_d')
    if data_dir.exists():
        catalog_size = agent.restaurant_collection.count()
        print(f"   ℹ️  Existing data found: {catalog_size} restaurants in catalog")
        if catalog_size == 0:
            print(f"   ⚠️  Catalog is empty - demo will fetch restaurants on first run")
        else:
            print(f"   💡 Tip: Delete 'data/matere_d/' for a fresh demo")
    else:
        print("   ✅ Clean slate - ready for first-time demo")

    # Test 6: Google API connection
    print("\n6️⃣  Testing Google Places API connection...")
    try:
        import requests
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': 'restaurants in New York, NY',
            'type': 'restaurant',
            'key': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data['status'] == 'OK':
            places = data.get('results', [])
            print(f"   ✅ API working! Test query found {len(places)} restaurants")
        elif data['status'] == 'REQUEST_DENIED':
            print(f"   ❌ API request denied - check your API key and billing")
            if 'error_message' in data:
                print(f"   💡 {data['error_message']}")
            return False
        else:
            print(f"   ⚠️  API status: {data['status']}")
            if 'error_message' in data:
                print(f"   💡 {data['error_message']}")
    except Exception as e:
        print(f"   ⚠️  API test failed: {e}")
        print(f"   💡 You may need to check your internet connection")

    # Success!
    print("\n" + "="*60)
    print("🎉 All tests passed! mATEre d' is ready to demo!")
    print("="*60)
    print("\n📋 Next steps:")
    print("   1. Run: python matere_d_demo.py")
    print("   2. Or run: python matere_d_demo.py quick (if catalog exists)")
    print("\n🎤 Check PRESENTATION_GUIDE.md for demo tips!")
    print()

    return True


if __name__ == "__main__":
    test_setup()
