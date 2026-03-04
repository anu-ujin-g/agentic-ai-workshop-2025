# 🍷 mATEre d' - Your AI Restaurant Sommelier

An intelligent restaurant recommendation agent that learns your dining preferences over time using Google Places API and machine learning.

## 🌟 Features

- **Smart Recommendations**: Natural language queries to find the perfect restaurant
- **Preference Learning**: Learns from your feedback to provide increasingly personalized suggestions
- **Google Places Integration**: Real-time restaurant data from Google Places API
- **Semantic Search**: Uses ChromaDB for intelligent matching beyond keyword search
- **Feedback System**: Track what you like, vibe scores, and dining experiences
- **Favorites Collection**: Automatically saves restaurants you loved

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Google Places API Key**: Get one from [Google Cloud Console](https://console.cloud.google.com/)
3. **Dependencies**:
   ```bash
   pip install chromadb requests python-dotenv
   ```

### Setup

1. Create a `.env` file in the notebooks directory:
   ```
   GOOGLE_PLACES_API_KEY=your_api_key_here
   ```

2. Run the demo:
   ```bash
   python matere_d_demo.py
   ```

   Or for a quick demo:
   ```bash
   python matere_d_demo.py quick
   ```

## 📖 How to Use

### Basic Usage

```python
from pathlib import Path
from matere_d_agent import SmartRestaurantAgent

# Initialize
agent = SmartRestaurantAgent(
    google_api_key="your_api_key",
    data_dir=Path('data/matere_d')
)

# Populate catalog (first time only)
agent.fetch_and_store_restaurants(location="New York, NY", limit=100)

# Get recommendations
restaurants, rec_id = agent.recommend_restaurants(
    query="romantic Italian restaurant for date night",
    n_results=5
)

# Provide feedback
agent.provide_feedback(
    recommendation_id=f"{rec_id}_{restaurants[0]['name']}",
    restaurant_name=restaurants[0]['name'],
    liked=True,
    vibe_score=5,
    visited=True,
    notes="Perfect ambiance!"
)

# View learned preferences
agent.show_learned_preferences()
agent.show_statistics()
```

### Query Examples

mATEre d' accepts natural language queries:

- `"romantic Italian restaurant for date night"`
- `"casual brunch spot with outdoor seating"`
- `"upscale steakhouse for business dinner"`
- `"family-friendly pizza place"`
- `"authentic sushi restaurant"`
- `"cheap Mexican food near Times Square"`

## 🧠 How It Learns

mATEre d' builds your dining profile through feedback:

1. **Feedback Collection**: Rate restaurants on multiple dimensions
   - Liked/Disliked
   - Vibe Score (1-5)
   - Query Relevance
   - Visit Status

2. **Preference Extraction**: Analyzes patterns in your feedback
   - Favorite cuisines
   - Price range preferences
   - Rating thresholds

3. **Smart Boosting**: Future recommendations favor your preferences
   - Restaurants matching your profile get boosted scores
   - High-rated favorites influence similar recommendations

## 📊 Architecture

```
mATEre d'/
├── matere_d_agent.py          # Main agent orchestrator
├── matere_d_preferences.py     # Preference learning system
├── matere_d_google_places.py   # Google Places API integration
├── matere_d_demo.py            # Presentation demo
└── data/matere_d/
    ├── restaurant_catalog/     # ChromaDB: Restaurant embeddings
    └── user_preferences/
        ├── user_preferences.db # SQLite: Feedback & learned prefs
        └── user_prefs_chroma/  # ChromaDB: Favorite restaurants
```

### Data Storage

- **Restaurant Catalog**: ChromaDB vector database for semantic search
- **User Preferences**: SQLite database for structured feedback data
- **Favorites**: Separate ChromaDB collection for loved restaurants

## 🎯 Presentation Tips

1. **Start Fresh**: Delete `data/matere_d/` folder for a clean demo
2. **Show the Learning**: Run multiple queries and show how preferences evolve
3. **Demonstrate Variety**: Try different cuisine types and vibes
4. **Highlight Feedback**: Show how feedback improves future recommendations

## 📝 API Costs

Google Places API usage:
- Text Search: $32 per 1,000 requests
- Free tier: $200 monthly credit
- Demo usage: ~60 restaurants = ~3-4 API calls = ~$0.10

## 🔮 Future Enhancements

- [ ] Real-time availability checking
- [ ] Multi-user support with user IDs
- [ ] Restaurant photos and reviews integration
- [ ] Export recommendations to calendar
- [ ] Social features (share favorites with friends)
- [ ] Location-based filtering and maps

## 🤝 Contributing

This is an educational project from the Agentic AI Workshop 2025.

## 📄 License

Educational use only.

---

**Built with ❤️ using Claude Code, ChromaDB, and Google Places API**
