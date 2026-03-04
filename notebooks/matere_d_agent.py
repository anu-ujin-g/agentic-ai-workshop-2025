"""
mATEre d' - Your AI Restaurant Sommelier

A smart restaurant recommendation agent that learns your dining preferences.
Combines Google Places API, ChromaDB restaurant search, and user preference tracking.
"""

import os
import chromadb
import requests
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from matere_d_preferences import UserPreferencesManager, UserFeedback
import uuid


class SmartRestaurantAgent:
    """Restaurant recommendation agent that learns from user feedback."""

    def __init__(self, google_api_key: str, data_dir: Path):
        self.google_api_key = google_api_key
        self.data_dir = Path(data_dir)

        # Initialize ChromaDB for restaurant catalog
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.data_dir / "restaurant_catalog")
        )
        self.restaurant_collection = self.chroma_client.get_or_create_collection(
            name="nyc_restaurants",
            metadata={"description": "NYC restaurant catalog from Google Places API"}
        )

        # Initialize user preferences manager
        self.prefs_manager = UserPreferencesManager(
            data_dir=self.data_dir / "user_preferences"
        )

    def fetch_and_store_restaurants(
        self,
        location: str = "New York, NY",
        radius_meters: int = 805,  # 0.5 miles in meters
        limit: int = 50,
        keyword: str = None
    ):
        """Fetch restaurants from Google Places API within 0.5 mile radius and store in ChromaDB.

        Args:
            location: Street address, intersection, landmark, or subway station
                     Examples: "5th Ave and 42nd St", "350 5th Avenue", "Grand Central Terminal"
            radius_meters: Search radius in meters (805m = 0.5 miles)
            limit: Maximum number of restaurants to fetch
            keyword: Optional keyword to filter results (e.g., "korean bbq", "pizza")
        """
        # Silently fetch restaurants

        # Google Places Nearby Search API (better for radius searches)
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

        # First, geocode the location to get lat/lng
        # Always append NYC to ensure results are in New York
        if 'new york' not in location.lower() and 'ny' not in location.lower():
            location = f"{location}, New York, NY"

        geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        geocode_params = {
            'address': location,
            'key': self.google_api_key
        }

        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_data = geocode_response.json()

        if geocode_data['status'] != 'OK' or not geocode_data.get('results'):
            print(f"\n❌ Could not find location: {location}")
            print(f"   Status: {geocode_data.get('status')}")
            if 'error_message' in geocode_data:
                print(f"   Error: {geocode_data['error_message']}")
            print(f"   Please use a valid address, intersection, or landmark")
            print(f"   Examples: 'Grand Central', '350 5th Ave', '5th Ave & 42nd St'\n")
            return 0

        lat_lng = geocode_data['results'][0]['geometry']['location']
        location_str = f"{lat_lng['lat']},{lat_lng['lng']}"
        found_address = geocode_data['results'][0]['formatted_address']
        print(f"✓ Found: {found_address}")

        params = {
            'location': location_str,
            'radius': radius_meters,
            'type': 'restaurant',
            'key': self.google_api_key
        }

        # Add keyword if provided for more targeted results
        if keyword:
            params['keyword'] = keyword

        all_places = []
        while len(all_places) < limit:
            response = requests.get(url, params=params)
            data = response.json()

            if data['status'] != 'OK':
                print(f"\n❌ Google Places API Error: {data.get('status')}")
                if data['status'] == 'REQUEST_DENIED':
                    print("\n🔧 How to fix REQUEST_DENIED:")
                    print("   1. Go to https://console.cloud.google.com/")
                    print("   2. Enable 'Places API' for your project")
                    print("   3. Set up billing (has free tier with $200/month credit)")
                    print("   4. Make sure your API key is correct in .env file")
                    if 'error_message' in data:
                        print(f"\n   📝 Google says: {data['error_message']}")
                elif 'error_message' in data:
                    print(f"   📝 Error message: {data['error_message']}")
                print()
                break

            all_places.extend(data.get('results', []))

            # Check for next page
            next_page_token = data.get('next_page_token')
            if not next_page_token or len(all_places) >= limit:
                break

            # Google requires a short delay before using next_page_token
            import time
            time.sleep(2)
            params['pagetoken'] = next_page_token

        count = 0
        for place in all_places[:limit]:
            # Extract restaurant types and identify cuisine
            types = place.get('types', [])

            # Map Google types to cuisine categories with EXTENSIVE dish keywords
            cuisine = "Restaurant"
            cuisine_keywords = []
            dish_keywords = []

            # Comprehensive cuisine and dish mapping
            cuisine_map = {
                'italian': {
                    'keywords': ['italian', 'trattoria', 'osteria', 'pizzeria', 'ristorante'],
                    'dishes': ['pizza', 'pasta', 'spaghetti', 'lasagna', 'ravioli', 'risotto',
                              'carbonara', 'marinara', 'penne', 'fettuccine', 'gnocchi', 'tiramisu',
                              'bruschetta', 'antipasto', 'gelato', 'calzone', 'margherita']
                },
                'chinese': {
                    'keywords': ['chinese', 'cantonese', 'szechuan', 'hunan', 'mandarin'],
                    'dishes': ['dim sum', 'dumpling', 'noodles', 'fried rice', 'lo mein', 'chow mein',
                              'kung pao', 'sweet and sour', 'general tso', 'wonton', 'spring roll',
                              'peking duck', 'mapo tofu', 'hot pot', 'bao', 'congee']
                },
                'japanese': {
                    'keywords': ['japanese', 'sushi bar', 'izakaya', 'ramen shop'],
                    'dishes': ['sushi', 'ramen', 'udon', 'soba', 'noodles', 'tempura', 'teriyaki',
                              'tonkatsu', 'gyoza', 'miso soup', 'edamame', 'yakitori', 'donburi',
                              'bento', 'sashimi', 'nigiri', 'maki', 'roll', 'katsu']
                },
                'mexican': {
                    'keywords': ['mexican', 'taqueria', 'cantina', 'tex-mex'],
                    'dishes': ['taco', 'burrito', 'quesadilla', 'enchilada', 'fajita', 'nachos',
                              'guacamole', 'salsa', 'tortilla', 'tamale', 'chimichanga', 'carnitas',
                              'al pastor', 'carne asada', 'queso', 'churro']
                },
                'indian': {
                    'keywords': ['indian', 'tandoori', 'curry house'],
                    'dishes': ['curry', 'tikka masala', 'biryani', 'naan', 'samosa', 'tandoori',
                              'korma', 'vindaloo', 'dal', 'paneer', 'chutney', 'pakora', 'dosa',
                              'idli', 'butter chicken', 'saag']
                },
                'thai': {
                    'keywords': ['thai'],
                    'dishes': ['pad thai', 'curry', 'noodles', 'tom yum', 'som tam', 'satay',
                              'green curry', 'red curry', 'massaman', 'basil', 'mango sticky rice',
                              'spring roll', 'larb', 'pad see ew', 'drunken noodles']
                },
                'vietnamese': {
                    'keywords': ['vietnamese'],
                    'dishes': ['pho', 'banh mi', 'spring roll', 'bun', 'vermicelli', 'noodles',
                              'rice noodles', 'noodle soup', 'com tam', 'bun bo hue', 'cao lau']
                },
                'korean': {
                    'keywords': ['korean', 'korean bbq', 'kbbq'],
                    'dishes': ['bbq', 'bulgogi', 'bibimbap', 'kimchi', 'korean fried chicken',
                              'japchae', 'tteokbokki', 'kimbap', 'galbi', 'samgyeopsal', 'jjigae']
                },
                'american': {
                    'keywords': ['american', 'diner', 'grill', 'steakhouse', 'bbq', 'smokehouse'],
                    'dishes': ['burger', 'steak', 'ribs', 'bbq', 'fries', 'wings', 'sandwich',
                              'hot dog', 'mac and cheese', 'fried chicken', 'brisket', 'pulled pork']
                },
                'french': {
                    'keywords': ['french', 'bistro', 'brasserie', 'cafe'],
                    'dishes': ['croissant', 'baguette', 'quiche', 'crepe', 'escargot', 'coq au vin',
                              'ratatouille', 'bouillabaisse', 'souffle', 'macaron', 'tart']
                },
                'mediterranean': {
                    'keywords': ['mediterranean', 'greek', 'lebanese'],
                    'dishes': ['hummus', 'falafel', 'gyro', 'shawarma', 'kebab', 'pita', 'tzatziki',
                              'dolma', 'moussaka', 'souvlaki', 'baklava', 'tabbouleh']
                },
                'spanish': {
                    'keywords': ['spanish', 'tapas bar'],
                    'dishes': ['tapas', 'paella', 'gazpacho', 'chorizo', 'tortilla', 'jamón',
                              'patatas bravas', 'croquetas', 'sangria']
                }
            }

            # Check types and name for cuisine and dishes
            types_str = ' '.join(types).lower()
            name_lower = place['name'].lower()
            search_text = f"{types_str} {name_lower}"

            # Prioritize checking name first for cuisine detection
            cuisine_found = False
            for cuisine_name, data in cuisine_map.items():
                # Check cuisine keywords in NAME first (more reliable than types)
                for keyword in data['keywords']:
                    if keyword in name_lower:
                        cuisine = cuisine_name.title()
                        cuisine_keywords.append(keyword)
                        cuisine_found = True
                        break
                if cuisine_found:
                    break

            # Then check for dish keywords in both name and types
            for cuisine_name, data in cuisine_map.items():
                for dish in data['dishes']:
                    if dish in search_text:
                        # Only update cuisine if we haven't found one yet
                        if not cuisine_found:
                            cuisine = cuisine_name.title()
                        dish_keywords.append(dish)
                        if len(dish_keywords) >= 5:  # Limit to top 5 dishes
                            break

            # Determine atmosphere/vibe from types
            atmosphere = []
            if 'bar' in types:
                atmosphere.append('bar')
            if 'cafe' in types or 'coffee' in types_str:
                atmosphere.append('casual cafe')
            if 'fine_dining' in types_str:
                atmosphere.append('upscale fine dining')
            if 'fast_food' in types_str or place.get('price_level', 2) == 1:
                atmosphere.append('quick casual')
            if place.get('price_level', 2) >= 3:
                atmosphere.append('upscale')

            # Price description
            price_level = place.get('price_level', 2)
            price_desc = {
                1: "cheap, budget-friendly, inexpensive, affordable",
                2: "moderately priced, mid-range",
                3: "upscale, expensive, fancy, high-end",
                4: "very expensive, luxury, fine dining, premium"
            }.get(price_level, "moderately priced")

            # Rating description
            rating = place.get('rating', 0)
            rating_desc = ""
            if rating >= 4.5:
                rating_desc = "highly rated, excellent reviews, top rated, popular"
            elif rating >= 4.0:
                rating_desc = "well-reviewed, good ratings, popular"
            elif rating >= 3.5:
                rating_desc = "decent reviews"

            # Build rich embedding text for semantic search with DISH FOCUS
            embedding_parts = [
                f"{place['name']}",
                f"{cuisine} restaurant",
            ]

            # CRITICAL: Add specific dish keywords for better matching
            if dish_keywords:
                # Put dishes EARLY in the embedding for higher weight
                embedding_parts.insert(1, f"specializes in {', '.join(dish_keywords)}")

            if cuisine_keywords:
                embedding_parts.append(f"{', '.join(cuisine_keywords)} cuisine")

            if atmosphere:
                embedding_parts.append(f"{', '.join(atmosphere)} atmosphere")

            embedding_parts.append(price_desc)

            if rating_desc:
                embedding_parts.append(rating_desc)

            if place.get('user_ratings_total', 0) > 1000:
                embedding_parts.append("very popular with many reviews")

            # Add neighborhood context
            if 'vicinity' in place:
                embedding_parts.append(f"located in {place['vicinity']}")

            embedding_text = ". ".join(embedding_parts) + "."

            # Add to ChromaDB
            try:
                self.restaurant_collection.add(
                    documents=[embedding_text],
                    metadatas=[{
                        'id': place['place_id'],
                        'name': place['name'],
                        'cuisine': cuisine,
                        'price_range': '$' * max(1, price_level),
                        'rating': rating,
                        'review_count': place.get('user_ratings_total', 0),
                        'address': place.get('vicinity', place.get('formatted_address', '')),
                        'phone': '',
                        'google_url': f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                    }],
                    ids=[f"google_{place['place_id']}"]
                )
                count += 1
            except Exception as e:
                print(f"Error adding {place['name']}: {e}")

        return count

    def recommend_restaurants(
        self,
        query: str,
        n_results: int = 5,
        use_preferences: bool = True
    ) -> List[Dict]:
        """Get restaurant recommendations, optionally using learned preferences."""

        # Check if user wants new/different places
        exclude_visited = any(word in query.lower() for word in ['new', 'different', 'another', 'try something', 'never been'])

        # First, get more results to filter from
        search_results = n_results * 5  # Get 5x more to filter

        if use_preferences:
            results = self.prefs_manager.get_recommendations_with_preferences(
                query=query,
                restaurant_collection=self.restaurant_collection,
                n_results=search_results
            )
            restaurants = []
            for r in results:
                # Convert boosted score to percentage (0-100%)
                # Score is based on similarity + preference boosts
                match_score = min(100, max(0, r['score'] * 100))
                restaurants.append({
                    **r['metadata'],
                    'match_score': match_score,
                    'original_distance': r['original_distance']
                })
        else:
            results = self.restaurant_collection.query(
                query_texts=[query],
                n_results=search_results
            )
            restaurants = []
            for id, metadata, distance in zip(
                results['ids'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
                # ChromaDB distance: lower is better (0 = perfect match)
                # Convert to similarity score: 100% = perfect, lower % = less similar
                # Typical distances are 0.3-1.5, so we normalize
                similarity = max(0, 1 - distance)  # 0 to 1
                match_score = similarity * 100  # Convert to percentage
                restaurants.append({
                    **metadata,
                    'match_score': match_score
                })

        # CRITICAL: Smart keyword filtering with cuisine awareness
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 2]  # Skip "at", "in", etc.

        # For "korean bbq" type queries, prioritize those with "korean" in cuisine
        primary_cuisine = None
        if 'korean' in query_words:
            primary_cuisine = 'korean'
        elif 'japanese' in query_words:
            primary_cuisine = 'japanese'
        elif 'chinese' in query_words:
            primary_cuisine = 'chinese'
        elif 'italian' in query_words:
            primary_cuisine = 'italian'
        elif 'mexican' in query_words:
            primary_cuisine = 'mexican'
        elif 'thai' in query_words:
            primary_cuisine = 'thai'
        elif 'indian' in query_words:
            primary_cuisine = 'indian'
        elif 'vietnamese' in query_words:
            primary_cuisine = 'vietnamese'
        elif 'french' in query_words:
            primary_cuisine = 'french'

        filtered_restaurants = []
        for restaurant in restaurants:
            cuisine_lower = restaurant['cuisine'].lower()
            name_lower = restaurant['name'].lower()
            combined = f"{cuisine_lower} {name_lower}"

            # Count how many query words match
            match_count = sum(1 for word in query_words if word in combined)

            # If we have a primary cuisine specified
            if primary_cuisine:
                # MUST have the primary cuisine
                if primary_cuisine in combined:
                    restaurant['match_score'] += match_count * 20  # Big boost
                    filtered_restaurants.append(restaurant)
            else:
                # No primary cuisine - just need any match
                if match_count > 0:
                    restaurant['match_score'] += match_count * 15
                    filtered_restaurants.append(restaurant)

        # If nothing found with primary cuisine, try without it
        if not filtered_restaurants and primary_cuisine:
            for restaurant in restaurants:
                cuisine_lower = restaurant['cuisine'].lower()
                name_lower = restaurant['name'].lower()
                combined = f"{cuisine_lower} {name_lower}"

                match_count = sum(1 for word in query_words if word in combined)
                if match_count > 0:
                    filtered_restaurants.append(restaurant)

        # Last resort: return original results
        if not filtered_restaurants:
            filtered_restaurants = restaurants

        # Filter by price range if specified in query
        price_filtered = []
        desired_price_level = None

        # Detect price keywords in query
        if any(word in query_lower for word in ['cheap', 'inexpensive', 'budget', 'affordable', 'value']):
            desired_price_level = '$'
        elif any(word in query_lower for word in ['expensive', 'fancy', 'upscale', 'fine dining', 'luxury', 'pricey']):
            desired_price_level = '$$$'
        elif any(word in query_lower for word in ['moderate', 'mid-range', 'medium']):
            desired_price_level = '$$'

        # Apply price filter if specified
        if desired_price_level:
            for restaurant in filtered_restaurants:
                if restaurant.get('price_range') == desired_price_level:
                    # Boost score for matching price range
                    restaurant['match_score'] += 10
                    price_filtered.append(restaurant)

            # If we found matches with desired price, use them
            if price_filtered:
                filtered_restaurants = price_filtered

        # Exclude visited restaurants if user wants new places
        if exclude_visited:
            # Get list of visited restaurants
            conn = sqlite3.connect(self.prefs_manager.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT rh.restaurant_name
                FROM user_feedback uf
                JOIN recommendation_history rh ON uf.recommendation_id = rh.recommendation_id
                WHERE uf.visited = 1
            """)
            visited_names = {row[0] for row in cursor.fetchall()}
            conn.close()

            # Filter out visited restaurants
            unvisited = [r for r in filtered_restaurants if r['name'] not in visited_names]

            # Use unvisited if we have any, otherwise keep all
            if unvisited:
                filtered_restaurants = unvisited

        # Sort by match score and return top N
        filtered_restaurants.sort(key=lambda x: x['match_score'], reverse=True)
        final_results = filtered_restaurants[:n_results]

        # Record recommendations
        recommendation_id = str(uuid.uuid4())
        for restaurant in final_results[:2]:  # Top 2 recommendations
            self.prefs_manager.record_recommendation(
                recommendation_id=f"{recommendation_id}_{restaurant['name']}",
                restaurant=restaurant,
                query=query
            )

        return final_results, recommendation_id

    def provide_feedback(
        self,
        recommendation_id: str,
        restaurant_name: str,
        liked: bool = None,
        vibe_score: int = None,
        fits_query: bool = None,
        visited: bool = None,
        notes: str = None
    ):
        """Provide feedback on a recommendation."""
        # Find restaurant in recent recommendations
        conn = sqlite3.connect(self.prefs_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT restaurant_id FROM recommendation_history
            WHERE recommendation_id = ? AND restaurant_name = ?
        """, (recommendation_id, restaurant_name))
        result = cursor.fetchone()
        conn.close()

        if not result:
            print(f"⚠️  Recommendation not found")
            return

        restaurant_id = result[0]

        feedback = UserFeedback(
            recommendation_id=recommendation_id,
            restaurant_id=restaurant_id,
            restaurant_name=restaurant_name,
            query="",  # Will be filled from DB
            liked=liked,
            vibe_score=vibe_score,
            fits_query=fits_query,
            visited=visited,
            notes=notes
        )

        self.prefs_manager.record_feedback(feedback)
        print(f"✅ Feedback recorded for {restaurant_name}")

    def show_learned_preferences(self):
        """Display learned preferences."""
        learned = self.prefs_manager.get_learned_preferences()

        print("\n" + "="*60)
        print("📊 YOUR LEARNED PREFERENCES")
        print("="*60)

        if not learned:
            print("No preferences learned yet. Provide more feedback!")
            return

        for pref_type, prefs in learned.items():
            print(f"\n{pref_type.upper()}:")
            for p in prefs:
                confidence_bar = "█" * int(p['confidence'] * 20)
                print(f"  {p['value']:20s} {confidence_bar} {p['confidence']:.1%}")

    def show_statistics(self):
        """Display usage statistics."""
        stats = self.prefs_manager.get_statistics()

        print("\n" + "="*60)
        print("📈 USAGE STATISTICS")
        print("="*60)
        print(f"Total recommendations: {stats['total_recommendations']}")
        print(f"Feedback provided: {stats['total_feedback']}")
        print(f"Liked: {stats['liked_count']} | Disliked: {stats['disliked_count']}")
        print(f"Like rate: {stats['like_rate']:.1%}")
        print(f"Average vibe score: {stats['avg_vibe_score']}/5.0")
        print(f"Favorites saved: {stats['favorites_count']}")

        if stats['top_cuisines']:
            print("\nTop Recommended Cuisines:")
            for item in stats['top_cuisines']:
                print(f"  - {item['cuisine']}: {item['count']} times")


# Usage Example
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # Initialize agent
    agent = SmartRestaurantAgent(
        google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
        data_dir=Path('data/restaurant_agent')
    )

    # STEP 1: Initial setup - fetch restaurants from Google Places (one-time)
    print("\n=== STEP 1: INITIAL SETUP ===")
    # Uncomment to populate catalog:
    # agent.fetch_and_store_restaurants(location="New York, NY", limit=100)

    # STEP 2: Get recommendations
    print("\n=== STEP 2: GET RECOMMENDATIONS ===")
    query = "romantic Italian restaurant for date night"
    restaurants, rec_id = agent.recommend_restaurants(
        query=query,
        n_results=5,
        use_preferences=True
    )

    print(f"\n🍽️  Top recommendations for: '{query}'\n")
    for i, r in enumerate(restaurants[:2], 1):
        print(f"{i}. {r['name']}")
        print(f"   Cuisine: {r['cuisine']}")
        print(f"   Price: {r['price_range']}")
        print(f"   Rating: {r['rating']}/5 ({r['review_count']} reviews)")
        print(f"   Match: {r['match_score']:.2%}")
        print(f"   {r['address']}")
        print()

    # STEP 3: Provide feedback
    print("\n=== STEP 3: PROVIDE FEEDBACK ===")
    # After visiting or deciding:
    agent.provide_feedback(
        recommendation_id=f"{rec_id}_{restaurants[0]['name']}",
        restaurant_name=restaurants[0]['name'],
        liked=True,
        vibe_score=5,
        fits_query=True,
        visited=True,
        notes="Perfect for our anniversary! Loved the ambiance"
    )

    # STEP 4: View learned preferences
    agent.show_learned_preferences()

    # STEP 5: View statistics
    agent.show_statistics()
