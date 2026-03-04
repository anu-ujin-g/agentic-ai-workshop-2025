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
        limit: int = 50
    ):
        """Fetch restaurants from Google Places API and store in ChromaDB."""
        print(f"🌐 Fetching restaurants from Google Places API...")

        # Google Places Text Search API
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': f'restaurants in {location}',
            'type': 'restaurant',
            'key': self.google_api_key
        }

        all_places = []
        while len(all_places) < limit:
            response = requests.get(url, params=params)
            data = response.json()

            if data['status'] != 'OK':
                print(f"⚠️  API error: {data.get('status')}")
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
            # Create embedding text
            types = ', '.join(place.get('types', []))
            embedding_text = (
                f"{place['name']} is a restaurant. "
                f"Rated {place.get('rating', 0)}/5 with {place.get('user_ratings_total', 0)} reviews. "
                f"Price: {place.get('price_level', 2) * '$'}."
            )

            # Add to ChromaDB
            try:
                self.restaurant_collection.add(
                    documents=[embedding_text],
                    metadatas=[{
                        'id': place['place_id'],
                        'name': place['name'],
                        'cuisine': types.split(',')[0].strip(),
                        'price_range': '$' * place.get('price_level', 2),
                        'rating': place.get('rating', 0),
                        'review_count': place.get('user_ratings_total', 0),
                        'address': place.get('formatted_address', ''),
                        'phone': '',
                        'google_url': f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                    }],
                    ids=[f"google_{place['place_id']}"]
                )
                count += 1
            except Exception as e:
                print(f"Error adding {place['name']}: {e}")

        print(f"✅ Added {count} restaurants to catalog")
        return count

    def recommend_restaurants(
        self,
        query: str,
        n_results: int = 5,
        use_preferences: bool = True
    ) -> List[Dict]:
        """Get restaurant recommendations, optionally using learned preferences."""

        if use_preferences:
            print("🧠 Using learned preferences to boost recommendations...")
            results = self.prefs_manager.get_recommendations_with_preferences(
                query=query,
                restaurant_collection=self.restaurant_collection,
                n_results=n_results
            )
            restaurants = []
            for r in results:
                restaurants.append({
                    **r['metadata'],
                    'match_score': r['score'],
                    'original_distance': r['original_distance']
                })
        else:
            print("🔍 Searching without preference boosting...")
            results = self.restaurant_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            restaurants = []
            for id, metadata, distance in zip(
                results['ids'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
                restaurants.append({
                    **metadata,
                    'match_score': 1 - distance
                })

        # Record recommendations
        recommendation_id = str(uuid.uuid4())
        for restaurant in restaurants[:2]:  # Top 2 recommendations
            self.prefs_manager.record_recommendation(
                recommendation_id=f"{recommendation_id}_{restaurant['name']}",
                restaurant=restaurant,
                query=query
            )

        return restaurants, recommendation_id

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
