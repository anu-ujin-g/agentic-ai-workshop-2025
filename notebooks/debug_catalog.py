"""
Debug script to see what's actually in the catalog
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from matere_d_agent import SmartRestaurantAgent

load_dotenv()

agent = SmartRestaurantAgent(
    google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
    data_dir=Path('data/matere_d')
)

catalog_size = agent.restaurant_collection.count()
print(f"Catalog size: {catalog_size} restaurants\n")

if catalog_size > 0:
    # Get all restaurants
    results = agent.restaurant_collection.get()

    print("First 10 restaurants in catalog:")
    print("="*70)

    for i in range(min(10, len(results['ids']))):
        metadata = results['metadatas'][i]
        document = results['documents'][i]

        print(f"\n{i+1}. {metadata['name']}")
        print(f"   Cuisine: {metadata['cuisine']}")
        print(f"   Embedding: {document[:200]}...")

    # Search for Korean
    print("\n\n" + "="*70)
    print("Searching for 'korean':")
    print("="*70)

    korean_results = agent.restaurant_collection.query(
        query_texts=["korean"],
        n_results=5
    )

    for i, metadata in enumerate(korean_results['metadatas'][0]):
        print(f"{i+1}. {metadata['name']} - {metadata['cuisine']}")

    # Search for BBQ
    print("\n" + "="*70)
    print("Searching for 'bbq':")
    print("="*70)

    bbq_results = agent.restaurant_collection.query(
        query_texts=["bbq"],
        n_results=5
    )

    for i, metadata in enumerate(bbq_results['metadatas'][0]):
        print(f"{i+1}. {metadata['name']} - {metadata['cuisine']}")

else:
    print("Catalog is empty! Run the demo first to build it.")
