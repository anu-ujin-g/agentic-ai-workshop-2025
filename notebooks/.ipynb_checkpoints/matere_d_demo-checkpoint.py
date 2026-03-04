"""
mATEre d' - Your AI Restaurant Sommelier
A smart restaurant recommendation agent that learns your preferences
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from matere_d_agent import SmartRestaurantAgent

# Load environment variables
load_dotenv()


def print_header():
    """Print a beautiful header for the demo."""
    print("\n" + "="*70)
    print("🍷  mATEre d' - Your AI Restaurant Sommelier  🍷")
    print("="*70)
    print("An intelligent agent that learns your dining preferences over time")
    print("="*70 + "\n")


def print_section(title):
    """Print a section header."""
    print("\n" + "─"*70)
    print(f"  {title}")
    print("─"*70 + "\n")


def demo_interactive():
    """Run an interactive demo of mATEre d'."""

    print_header()

    # Initialize the agent
    print("🔧 Initializing mATEre d'...")
    agent = SmartRestaurantAgent(
        google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
        data_dir=Path('data/matere_d')
    )
    print("✅ Agent initialized!\n")

    # Check if catalog exists
    catalog_size = agent.restaurant_collection.count()

    if catalog_size == 0:
        print_section("STEP 1: Building Restaurant Catalog")
        print("📚 First time setup - fetching restaurants from Google Places API...")
        print("   This may take a minute...\n")

        count = agent.fetch_and_store_restaurants(
            location="New York, NY",
            limit=60  # Start with 60 restaurants
        )
        print(f"\n✨ Successfully cataloged {count} restaurants!")
    else:
        print(f"📚 Restaurant catalog already loaded: {catalog_size} restaurants")

    # Get recommendations
    print_section("STEP 2: Getting Personalized Recommendations")

    # Demo query
    query = "romantic Italian restaurant for date night"
    print(f"🔍 Your query: \"{query}\"\n")
    print("🧠 Analyzing preferences and searching...\n")

    restaurants, rec_id = agent.recommend_restaurants(
        query=query,
        n_results=5,
        use_preferences=True
    )

    # Display top recommendations
    print("🍽️  TOP RECOMMENDATIONS:\n")
    for i, r in enumerate(restaurants[:3], 1):
        print(f"  {i}. {r['name']}")
        print(f"     └─ {r['cuisine']} • {r['price_range']} • ⭐ {r['rating']}/5 ({r['review_count']} reviews)")
        print(f"     └─ Match Score: {r['match_score']:.1%}")
        print(f"     └─ {r['address']}")
        print()

    # Simulate user feedback
    print_section("STEP 3: Learning from Your Feedback")

    print("💭 Imagine you visited the top recommendation and loved it!\n")
    print(f"   Restaurant: {restaurants[0]['name']}")
    print("   Your feedback:")
    print("   • Liked: ✅ Yes")
    print("   • Vibe Score: ⭐⭐⭐⭐⭐ (5/5)")
    print("   • Visited: ✅ Yes")
    print("   • Notes: 'Perfect ambiance for our anniversary!'\n")

    agent.provide_feedback(
        recommendation_id=f"{rec_id}_{restaurants[0]['name']}",
        restaurant_name=restaurants[0]['name'],
        liked=True,
        vibe_score=5,
        fits_query=True,
        visited=True,
        notes="Perfect ambiance for our anniversary!"
    )

    print("✅ Feedback recorded! mATEre d' is learning your preferences...")

    # Show learned preferences
    print_section("STEP 4: Your Learned Preferences")
    agent.show_learned_preferences()

    # Show statistics
    print_section("STEP 5: Usage Statistics")
    agent.show_statistics()

    # Future recommendations
    print_section("How mATEre d' Gets Smarter")
    print("🎯 As you provide more feedback, mATEre d' will:")
    print("   • Learn your favorite cuisines")
    print("   • Understand your price preferences")
    print("   • Remember places you loved")
    print("   • Boost similar restaurants in future recommendations")
    print("\n💡 Try different queries and provide feedback to build your profile!")

    print("\n" + "="*70)
    print("Thank you for trying mATEre d'! 🍷")
    print("="*70 + "\n")


def demo_quick():
    """Quick demo showing just the recommendation flow."""

    print_header()

    agent = SmartRestaurantAgent(
        google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
        data_dir=Path('data/matere_d')
    )

    # Example queries to showcase
    queries = [
        "romantic Italian restaurant for date night",
        "casual brunch spot with outdoor seating",
        "authentic sushi restaurant"
    ]

    for query in queries:
        print(f"\n🔍 Query: \"{query}\"\n")

        restaurants, _ = agent.recommend_restaurants(
            query=query,
            n_results=3,
            use_preferences=True
        )

        for i, r in enumerate(restaurants, 1):
            print(f"{i}. {r['name']} - {r['cuisine']} • {r['price_range']} • ⭐ {r['rating']}/5")

        print()


if __name__ == "__main__":
    import sys

    # Check for command line argument
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        demo_quick()
    else:
        demo_interactive()
