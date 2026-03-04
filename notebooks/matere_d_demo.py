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


def demo_interactive():
    """Run an interactive demo of mATEre d'."""

    # Simple header
    print("\nWelcome to mATEre d'!\n")

    # Initialize the agent
    agent = SmartRestaurantAgent(
        google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
        data_dir=Path('data/matere_d')
    )

    # Get natural language input
    full_query = input("What are you craving? ").strip()
    if not full_query:
        full_query = "korean bbq near times square"

    # Extract location from query
    location_keywords = ['near', 'at', 'around', 'by', 'in']
    location = None
    query = full_query

    for keyword in location_keywords:
        if keyword in full_query.lower():
            parts = full_query.lower().split(keyword, 1)
            if len(parts) == 2:
                query = parts[0].strip()
                location = parts[1].strip()
                break

    # If no location found in query, ask for it
    if not location:
        location = input("Where are you? ").strip()
        if not location:
            location = "Times Square, New York"

    # Always clear and rebuild catalog with query-specific keyword
    # This ensures we get relevant restaurants for the specific query
    existing_ids = agent.restaurant_collection.get()['ids']
    if existing_ids:
        agent.restaurant_collection.delete(ids=existing_ids)

    count = agent.fetch_and_store_restaurants(
        location=location,
        radius_meters=805,  # 0.5 miles
        limit=60,
        keyword=query  # Use the query as keyword for targeted results
    )

    if count == 0:
        print("\n⚠️  No restaurants found.\n")
        return

    # Track shown restaurants to avoid repeats
    shown_restaurant_ids = set()

    while True:
        # Get recommendations
        restaurants, rec_id = agent.recommend_restaurants(
            query=query,
            n_results=10,  # Get more so we can show different ones
            use_preferences=True
        )

        # Check if we got results
        if not restaurants or len(restaurants) == 0:
            print("No restaurants found.\n")
            return

        # Filter out already shown restaurants
        new_restaurants = [r for r in restaurants if r['name'] not in shown_restaurant_ids]

        if not new_restaurants:
            print("No more restaurants to show.\n")
            return

        # Show top 2 new restaurants
        display_restaurants = new_restaurants[:2]
        for r in display_restaurants:
            shown_restaurant_ids.add(r['name'])

        # Display results
        print()
        for i, r in enumerate(display_restaurants, 1):
            print(f"{i}. {r['name']}")
            print(f"   {r['cuisine']} • {r['price_range']} • ⭐ {r['rating']}/5 ({r['review_count']} reviews)")
            print(f"   Match: {r['match_score']:.1f}%")
            print(f"   {r['address']}")
            print()

        # Ask if results are good
        satisfaction_input = input("Are these good, or want to see more? ").strip().lower()

        # Check if user wants different results
        if any(word in satisfaction_input for word in ['more', 'different', 'other', 'else', 'another', 'next']):
            print()
            continue  # Show next set of restaurants

        # User is satisfied, ask for feedback
        break

    # Ask for feedback with natural language
    feedback_input = input("Want to give feedback? ").strip()

    # Simple parsing - if they mention a restaurant, save feedback
    if feedback_input and feedback_input.lower() not in ['no', 'nah', 'no thanks', 'pass', 'skip']:
        # Try to detect which restaurant (1 or 2)
        restaurant_index = None
        if 'first' in feedback_input.lower() or '1' in feedback_input:
            restaurant_index = 0
        elif 'second' in feedback_input.lower() or '2' in feedback_input:
            restaurant_index = 1
        elif len(display_restaurants) > 0:
            restaurant_index = 0  # Default to first if unclear

        if restaurant_index is not None and restaurant_index < len(display_restaurants):
            restaurant = display_restaurants[restaurant_index]

            # Detect sentiment
            liked = None
            if any(word in feedback_input.lower() for word in ['love', 'great', 'awesome', 'perfect', 'amazing']):
                liked = True
            elif any(word in feedback_input.lower() for word in ['bad', 'hate', 'terrible', 'awful']):
                liked = False

            # Try to extract vibe score
            vibe_score = None
            for i in range(1, 6):
                if str(i) in feedback_input:
                    vibe_score = i
                    break

            # Detect if they visited
            visited = None
            if any(word in feedback_input.lower() for word in ['visited', 'went', 'been there', 'tried it']):
                visited = True

            # Save feedback
            agent.provide_feedback(
                recommendation_id=f"{rec_id}_{restaurant['name']}",
                restaurant_name=restaurant['name'],
                liked=liked,
                vibe_score=vibe_score,
                fits_query=True,
                visited=visited,
                notes=feedback_input
            )

            print("✅ Thanks!\n")
        else:
            print()
    else:
        print()


def demo_quick():
    """Quick demo showing just the recommendation flow."""

    print_header()

    agent = SmartRestaurantAgent(
        google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
        data_dir=Path('data/matere_d')
    )

    # Check if catalog exists
    catalog_size = agent.restaurant_collection.count()
    if catalog_size == 0:
        print("⚠️  No restaurants in catalog. Please run the full demo first:")
        print("   python matere_d_demo.py")
        return

    print(f"📚 Using catalog of {catalog_size} restaurants\n")

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

        if restaurants:
            for i, r in enumerate(restaurants, 1):
                print(f"{i}. {r['name']} - {r['cuisine']} • {r['price_range']} • ⭐ {r['rating']}/5")
        else:
            print("   No matches found")

        print()


if __name__ == "__main__":
    import sys

    # Check for command line argument
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        demo_quick()
    else:
        demo_interactive()
