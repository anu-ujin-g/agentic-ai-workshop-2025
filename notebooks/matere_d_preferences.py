"""
mATEre d' - User Preferences and Learning System

Tracks user feedback and learns their "vibe" over time to provide
increasingly personalized restaurant recommendations.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import chromadb
from dataclasses import dataclass, asdict


@dataclass
class UserFeedback:
    """User feedback on a restaurant recommendation."""
    recommendation_id: str
    restaurant_id: str
    restaurant_name: str
    query: str  # Original user query
    liked: Optional[bool] = None  # True = like, False = dislike, None = neutral
    vibe_score: Optional[int] = None  # 1-5 scale
    fits_query: Optional[bool] = None  # Was it relevant to the query?
    visited: Optional[bool] = None  # Did they actually go?
    notes: Optional[str] = None  # Free-form notes
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class UserPreferencesManager:
    """Manages user preferences and learning from feedback."""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # SQLite for structured preference data
        self.db_path = self.data_dir / "user_preferences.db"
        self.init_database()

        # ChromaDB for user's favorite restaurants (separate from main restaurant catalog)
        self.prefs_chroma_client = chromadb.PersistentClient(
            path=str(self.data_dir / "user_prefs_chroma")
        )
        self.favorites_collection = self.prefs_chroma_client.get_or_create_collection(
            name="user_favorites",
            metadata={"description": "Restaurants the user loves"}
        )

    def init_database(self):
        """Initialize SQLite database for preference tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for recommendation history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id TEXT UNIQUE,
                restaurant_id TEXT,
                restaurant_name TEXT,
                cuisine TEXT,
                price_range TEXT,
                query TEXT,
                timestamp TEXT
            )
        """)

        # Table for user feedback
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id TEXT,
                liked INTEGER,  -- 1 = like, 0 = dislike, NULL = neutral
                vibe_score INTEGER,  -- 1-5
                fits_query INTEGER,  -- 1 = yes, 0 = no
                visited INTEGER,  -- 1 = yes, 0 = no
                notes TEXT,
                timestamp TEXT,
                FOREIGN KEY (recommendation_id) REFERENCES recommendation_history(recommendation_id)
            )
        """)

        # Table for learned preferences
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                preference_type TEXT,  -- 'cuisine', 'price', 'attribute', etc.
                preference_value TEXT,
                confidence REAL,  -- 0-1 score based on feedback
                updated_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def record_recommendation(
        self,
        recommendation_id: str,
        restaurant: Dict,
        query: str
    ):
        """Record that a recommendation was made."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO recommendation_history
            (recommendation_id, restaurant_id, restaurant_name, cuisine, price_range, query, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            recommendation_id,
            restaurant.get('id', ''),
            restaurant['name'],
            restaurant.get('cuisine', ''),
            restaurant.get('price_range', '$$'),
            query,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def record_feedback(self, feedback: UserFeedback):
        """Record user feedback on a recommendation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_feedback
            (recommendation_id, liked, vibe_score, fits_query, visited, notes, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            feedback.recommendation_id,
            1 if feedback.liked else 0 if feedback.liked is not None else None,
            feedback.vibe_score,
            1 if feedback.fits_query else 0 if feedback.fits_query is not None else None,
            1 if feedback.visited else 0 if feedback.visited is not None else None,
            feedback.notes,
            feedback.timestamp
        ))

        conn.commit()
        conn.close()

        # If user loved it, add to favorites collection
        if feedback.liked and feedback.vibe_score and feedback.vibe_score >= 4:
            self._add_to_favorites(feedback.restaurant_id, feedback.restaurant_name)

        # Update learned preferences
        self._update_learned_preferences(feedback)

    def _add_to_favorites(self, restaurant_id: str, restaurant_name: str):
        """Add restaurant to user's favorites in ChromaDB."""
        try:
            # Get full restaurant details
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT restaurant_name, cuisine, price_range
                FROM recommendation_history
                WHERE restaurant_id = ?
                LIMIT 1
            """, (restaurant_id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                name, cuisine, price = result
                embedding_text = f"{name} - {cuisine} restaurant that user loves. Price: {price}"

                self.favorites_collection.add(
                    documents=[embedding_text],
                    metadatas=[{
                        'restaurant_id': restaurant_id,
                        'name': name,
                        'cuisine': cuisine,
                        'price_range': price,
                        'added_at': datetime.now().isoformat()
                    }],
                    ids=[f"fav_{restaurant_id}"]
                )
                print(f"✅ Added {name} to favorites")
        except Exception as e:
            print(f"Error adding to favorites: {e}")

    def _update_learned_preferences(self, feedback: UserFeedback):
        """Update learned preferences based on feedback."""
        if feedback.liked is None:
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get restaurant details
        cursor.execute("""
            SELECT cuisine, price_range
            FROM recommendation_history
            WHERE recommendation_id = ?
        """, (feedback.recommendation_id,))
        result = cursor.fetchone()

        if result:
            cuisine, price = result

            # Update cuisine preference
            if feedback.liked:
                self._increment_preference(cursor, 'cuisine', cuisine, 0.1)
            else:
                self._increment_preference(cursor, 'cuisine', cuisine, -0.05)

            # Update price preference
            if feedback.liked:
                self._increment_preference(cursor, 'price', price, 0.1)

        conn.commit()
        conn.close()

    def _increment_preference(
        self,
        cursor,
        pref_type: str,
        pref_value: str,
        delta: float
    ):
        """Increment or decrement preference confidence."""
        cursor.execute("""
            SELECT confidence FROM learned_preferences
            WHERE preference_type = ? AND preference_value = ?
        """, (pref_type, pref_value))

        result = cursor.fetchone()

        if result:
            new_confidence = max(0, min(1, result[0] + delta))
            cursor.execute("""
                UPDATE learned_preferences
                SET confidence = ?, updated_at = ?
                WHERE preference_type = ? AND preference_value = ?
            """, (new_confidence, datetime.now().isoformat(), pref_type, pref_value))
        else:
            initial_confidence = max(0, min(1, 0.5 + delta))
            cursor.execute("""
                INSERT INTO learned_preferences
                (preference_type, preference_value, confidence, updated_at)
                VALUES (?, ?, ?, ?)
            """, (pref_type, pref_value, initial_confidence, datetime.now().isoformat()))

    def get_learned_preferences(self) -> Dict[str, List[Dict]]:
        """Get all learned preferences grouped by type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT preference_type, preference_value, confidence, updated_at
            FROM learned_preferences
            WHERE confidence > 0.3
            ORDER BY preference_type, confidence DESC
        """)

        preferences = {}
        for row in cursor.fetchall():
            pref_type, pref_value, confidence, updated_at = row
            if pref_type not in preferences:
                preferences[pref_type] = []
            preferences[pref_type].append({
                'value': pref_value,
                'confidence': confidence,
                'updated_at': updated_at
            })

        conn.close()
        return preferences

    def get_recommendations_with_preferences(
        self,
        query: str,
        restaurant_collection: chromadb.Collection,
        n_results: int = 10
    ) -> List[Dict]:
        """Get recommendations boosted by learned preferences."""
        # Get learned preferences
        learned = self.get_learned_preferences()

        # Build enhanced query using preferences
        enhanced_query = query
        if 'cuisine' in learned:
            top_cuisines = [p['value'] for p in learned['cuisine'][:3]]
            enhanced_query += f" {' '.join(top_cuisines)}"

        # Search with enhanced query
        results = restaurant_collection.query(
            query_texts=[enhanced_query],
            n_results=n_results
        )

        # Boost scores based on learned preferences
        scored_results = []
        for i, (id, metadata, distance) in enumerate(zip(
            results['ids'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            score = 1 - distance  # Base similarity score

            # Boost by cuisine preference
            if 'cuisine' in learned:
                for pref in learned['cuisine']:
                    if metadata.get('cuisine') == pref['value']:
                        score += pref['confidence'] * 0.2

            # Boost by price preference
            if 'price' in learned:
                for pref in learned['price']:
                    if metadata.get('price_range') == pref['value']:
                        score += pref['confidence'] * 0.1

            scored_results.append({
                'id': id,
                'metadata': metadata,
                'score': score,
                'original_distance': distance
            })

        # Re-sort by boosted score
        scored_results.sort(key=lambda x: x['score'], reverse=True)

        return scored_results

    def get_statistics(self) -> Dict:
        """Get usage and preference statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total recommendations
        cursor.execute("SELECT COUNT(*) FROM recommendation_history")
        total_recommendations = cursor.fetchone()[0]

        # Total feedback entries
        cursor.execute("SELECT COUNT(*) FROM user_feedback")
        total_feedback = cursor.fetchone()[0]

        # Liked vs disliked
        cursor.execute("SELECT COUNT(*) FROM user_feedback WHERE liked = 1")
        liked_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM user_feedback WHERE liked = 0")
        disliked_count = cursor.fetchone()[0]

        # Average vibe score
        cursor.execute("SELECT AVG(vibe_score) FROM user_feedback WHERE vibe_score IS NOT NULL")
        avg_vibe = cursor.fetchone()[0] or 0

        # Most recommended cuisines
        cursor.execute("""
            SELECT cuisine, COUNT(*) as count
            FROM recommendation_history
            WHERE cuisine != ''
            GROUP BY cuisine
            ORDER BY count DESC
            LIMIT 5
        """)
        top_cuisines = cursor.fetchall()

        conn.close()

        return {
            'total_recommendations': total_recommendations,
            'total_feedback': total_feedback,
            'liked_count': liked_count,
            'disliked_count': disliked_count,
            'like_rate': liked_count / total_feedback if total_feedback > 0 else 0,
            'avg_vibe_score': round(avg_vibe, 2),
            'top_cuisines': [{'cuisine': c, 'count': n} for c, n in top_cuisines],
            'favorites_count': self.favorites_collection.count()
        }


# Example usage
if __name__ == "__main__":
    from pathlib import Path

    # Initialize preference manager
    prefs_manager = UserPreferencesManager(
        data_dir=Path("data/user_preferences")
    )

    # Simulate recording a recommendation
    recommendation_id = "rec_001"
    restaurant = {
        'id': 'rest_001',
        'name': 'La Bella Italia',
        'cuisine': 'Italian',
        'price_range': '$$'
    }

    prefs_manager.record_recommendation(
        recommendation_id=recommendation_id,
        restaurant=restaurant,
        query="Italian pasta dinner"
    )

    # Simulate user feedback
    feedback = UserFeedback(
        recommendation_id=recommendation_id,
        restaurant_id=restaurant['id'],
        restaurant_name=restaurant['name'],
        query="Italian pasta dinner",
        liked=True,
        vibe_score=5,
        fits_query=True,
        visited=True,
        notes="Amazing carbonara! Perfect vibe for date night"
    )

    prefs_manager.record_feedback(feedback)

    # Get learned preferences
    learned = prefs_manager.get_learned_preferences()
    print("\n📊 Learned Preferences:")
    for pref_type, prefs in learned.items():
        print(f"\n{pref_type.title()}:")
        for p in prefs:
            print(f"  - {p['value']}: {p['confidence']:.2%} confidence")

    # Get statistics
    stats = prefs_manager.get_statistics()
    print("\n📈 Usage Statistics:")
    print(f"Total recommendations: {stats['total_recommendations']}")
    print(f"Like rate: {stats['like_rate']:.1%}")
    print(f"Average vibe score: {stats['avg_vibe_score']}/5")
    print(f"Favorites: {stats['favorites_count']} restaurants")
