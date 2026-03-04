"""
Google Places API Integration for Restaurant Agent
FREE tier: $200/month credit = ~6,000 restaurant searches
"""

import googlemaps
import os
from datetime import datetime
from typing import List, Dict, Optional
import chromadb


class GooglePlacesRestaurantAPI:
    """Wrapper for Google Places API with restaurant-specific methods."""

    def __init__(self, api_key: str):
        self.gmaps = googlemaps.Client(key=api_key)
        self.api_calls = 0  # Track usage

    def search_restaurants(
        self,
        query: str = "restaurants",
        location: str = "New York, NY",
        radius: int = 5000,
        limit: int = 20,
        price_levels: Optional[List[int]] = None
    ) -> List[Dict]:
        """Search for restaurants with filters.

        Args:
            query: Search query (e.g., "Italian restaurants", "sushi")
            location: Location string or (lat, lng) tuple
            radius: Search radius in meters
            limit: Max number of results
            price_levels: List of price levels 0-4 (0=Free, 1=$, 2=$$, 3=$$$, 4=$$$$)

        Returns:
            List of restaurant dictionaries
        """
        # Geocode location if it's a string
        if isinstance(location, str):
            geocode_result = self.gmaps.geocode(location)
            if not geocode_result:
                raise ValueError(f"Could not geocode location: {location}")
            lat_lng = geocode_result[0]['geometry']['location']
            location = (lat_lng['lat'], lat_lng['lng'])
            self.api_calls += 1

        # Search for places
        places_result = self.gmaps.places_nearby(
            location=location,
            radius=radius,
            type='restaurant',
            keyword=query
        )
        self.api_calls += 1

        restaurants = []
        for place in places_result.get('results', [])[:limit]:
            # Filter by price level if specified
            if price_levels and place.get('price_level') not in price_levels:
                continue

            restaurant = {
                'id': place['place_id'],
                'name': place['name'],
                'rating': place.get('rating', 0),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'price_level': place.get('price_level', 2),
                'address': place.get('vicinity', ''),
                'location': place['geometry']['location'],
                'types': place.get('types', []),
                'open_now': place.get('opening_hours', {}).get('open_now'),
            }
            restaurants.append(restaurant)

        return restaurants

    def get_restaurant_details(
        self,
        place_id: str,
        include_reviews: bool = True
    ) -> Dict:
        """Get detailed information about a specific restaurant.

        Args:
            place_id: Google Place ID
            include_reviews: Whether to fetch reviews (uses more API credits)

        Returns:
            Detailed restaurant information
        """
        fields = [
            'name', 'rating', 'price_level', 'formatted_address',
            'formatted_phone_number', 'website', 'opening_hours',
            'user_ratings_total', 'types', 'url'
        ]

        if include_reviews:
            fields.append('reviews')

        place_details = self.gmaps.place(
            place_id=place_id,
            fields=fields
        )
        self.api_calls += 1

        result = place_details.get('result', {})

        # Parse opening hours
        opening_hours = result.get('opening_hours', {})
        hours_text = opening_hours.get('weekday_text', [])

        return {
            'id': place_id,
            'name': result.get('name'),
            'rating': result.get('rating', 0),
            'user_ratings_total': result.get('user_ratings_total', 0),
            'price_level': result.get('price_level', 2),
            'address': result.get('formatted_address'),
            'phone': result.get('formatted_phone_number'),
            'website': result.get('website'),
            'google_maps_url': result.get('url'),
            'opening_hours': hours_text,
            'types': result.get('types', []),
            'reviews': result.get('reviews', [])[:5] if include_reviews else []
        }

    def get_current_busyness(self, place_id: str) -> Optional[Dict]:
        """Get current busyness information for a restaurant.

        Note: This is experimental and may not work for all places.
        Google doesn't officially provide real-time busyness via API.
        """
        # This would require using the popular times feature
        # which is not officially in the API
        # You might need to use a third-party scraper or wait for official support
        return None

    def populate_chromadb(
        self,
        collection: chromadb.Collection,
        locations: List[str] = ["New York, NY"],
        queries: List[str] = ["restaurants", "italian restaurants", "japanese restaurants",
                              "mexican restaurants", "chinese restaurants", "american restaurants"],
        limit_per_query: int = 20
    ) -> int:
        """Populate ChromaDB with restaurants from Google Places.

        Args:
            collection: ChromaDB collection to populate
            locations: List of location strings
            queries: List of search queries to diversify results
            limit_per_query: Max results per query

        Returns:
            Total number of restaurants added
        """
        print("🌐 Populating ChromaDB with Google Places data...")

        added_ids = set()
        total_added = 0

        for location in locations:
            for query in queries:
                print(f"  Searching: {query} in {location}...")

                try:
                    restaurants = self.search_restaurants(
                        query=query,
                        location=location,
                        limit=limit_per_query
                    )

                    for restaurant in restaurants:
                        # Skip duplicates
                        if restaurant['id'] in added_ids:
                            continue

                        # Get detailed info
                        try:
                            details = self.get_restaurant_details(
                                restaurant['id'],
                                include_reviews=False  # Save API credits
                            )

                            # Create embedding text
                            cuisine = self._extract_cuisine(details['types'])
                            price_symbols = '$' * (details['price_level'] if details['price_level'] > 0 else 2)

                            embedding_text = (
                                f"{details['name']} is a {cuisine} restaurant. "
                                f"Rated {details['rating']}/5 with {details['user_ratings_total']} reviews. "
                                f"Price range: {price_symbols}. "
                                f"Located at {details['address']}."
                            )

                            # Add to ChromaDB
                            collection.add(
                                documents=[embedding_text],
                                metadatas=[{
                                    'name': details['name'],
                                    'cuisine': cuisine,
                                    'price_range': price_symbols,
                                    'rating': details['rating'],
                                    'review_count': details['user_ratings_total'],
                                    'address': details['address'],
                                    'phone': details.get('phone', ''),
                                    'website': details.get('website', ''),
                                    'google_place_id': details['id'],
                                    'added_at': datetime.now().isoformat()
                                }],
                                ids=[f"google_{details['id']}"]
                            )

                            added_ids.add(restaurant['id'])
                            total_added += 1

                        except Exception as e:
                            print(f"    Error getting details for {restaurant['name']}: {e}")
                            continue

                except Exception as e:
                    print(f"  Error searching {query}: {e}")
                    continue

        print(f"\n✅ Added {total_added} unique restaurants to ChromaDB")
        print(f"📊 Total API calls used: {self.api_calls}")
        print(f"💰 Estimated cost: ${self.api_calls * 0.032:.2f} (within free $200 credit)")

        return total_added

    def _extract_cuisine(self, types: List[str]) -> str:
        """Extract cuisine type from Google place types."""
        # Map Google types to cuisine names
        cuisine_map = {
            'italian_restaurant': 'Italian',
            'japanese_restaurant': 'Japanese',
            'chinese_restaurant': 'Chinese',
            'mexican_restaurant': 'Mexican',
            'indian_restaurant': 'Indian',
            'french_restaurant': 'French',
            'thai_restaurant': 'Thai',
            'korean_restaurant': 'Korean',
            'vietnamese_restaurant': 'Vietnamese',
            'american_restaurant': 'American',
            'seafood_restaurant': 'Seafood',
            'steakhouse': 'Steakhouse',
            'pizza_restaurant': 'Pizza',
            'sushi_restaurant': 'Japanese',
        }

        for place_type in types:
            if place_type in cuisine_map:
                return cuisine_map[place_type]

        return 'General'


# Usage Example
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # Initialize API
    google_api = GooglePlacesRestaurantAPI(
        api_key=os.getenv('GOOGLE_MAPS_API_KEY')
    )

    # Initialize ChromaDB
    chroma_client = chromadb.Client()
    try:
        chroma_client.delete_collection("nyc_restaurants_google")
    except:
        pass
    collection = chroma_client.create_collection("nyc_restaurants_google")

    # Populate with NYC restaurants
    total = google_api.populate_chromadb(
        collection=collection,
        locations=["New York, NY"],
        queries=[
            "restaurants",
            "italian restaurants",
            "japanese sushi restaurants",
            "mexican restaurants",
            "chinese restaurants",
            "french restaurants",
            "indian restaurants",
            "american steakhouse"
        ],
        limit_per_query=15
    )

    print(f"\n✅ Setup complete! {total} restaurants in database")
    print(f"📊 Collection size: {collection.count()}")

    # Test search
    print("\n🔍 Testing search for 'romantic italian dinner'...")
    results = collection.query(
        query_texts=["romantic italian dinner with pasta"],
        n_results=3
    )

    print("\nTop 3 matches:")
    for i, metadata in enumerate(results['metadatas'][0], 1):
        print(f"{i}. {metadata['name']} - {metadata['cuisine']} - {metadata['price_range']}")
        print(f"   Rating: {metadata['rating']}/5 ({metadata['review_count']} reviews)")
        print(f"   {metadata['address']}")
