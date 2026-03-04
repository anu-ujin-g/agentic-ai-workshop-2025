# 🎤 mATEre d' - Presentation Guide

## Quick Setup (Before Demo)

```bash
# 1. Make sure your .env file has your Google API key
# GOOGLE_PLACES_API_KEY=your_key_here

# 2. (Optional) Delete old data for fresh demo
rm -rf data/matere_d/

# 3. Run the demo
python matere_d_demo.py
```

## 🎯 Demo Flow (5-7 minutes)

### 1. **Introduction** (30 seconds)
"I'd like to introduce mATEre d' - your AI Restaurant Sommelier. It's an intelligent agent that learns your dining preferences over time and provides increasingly personalized restaurant recommendations."

### 2. **Show the Problem** (30 seconds)
"Ever struggle to find restaurants that match your vibe? Search engines give you popular places, but they don't know YOUR taste. mATEre d' solves this by learning from your feedback."

### 3. **Run the Demo** (3-4 minutes)
```bash
python matere_d_demo.py
```

**While it runs, narrate:**
- **Step 1**: "First, it builds a restaurant catalog from Google Places API"
- **Step 2**: "Watch it process a natural language query - no structured input needed"
- **Step 3**: "See how it learns from feedback - liked, vibe score, visit status"
- **Step 4**: "These are the learned preferences it extracted"
- **Step 5**: "Statistics show how the system improves over time"

### 4. **Highlight Key Features** (1-2 minutes)

**Architecture:**
- "Two separate databases: ChromaDB for semantic search, SQLite for preferences"
- "Google Places API for real-time restaurant data"
- "Natural language queries using embeddings"

**Intelligence:**
- "Learns preferences from multi-dimensional feedback"
- "Automatically identifies favorite cuisines and price ranges"
- "Boosts future recommendations based on your profile"

### 5. **Show the Code** (1-2 minutes)

Open `matere_d_demo.py` and highlight:
```python
# Simple natural language query
query = "romantic Italian restaurant for date night"

# Get personalized recommendations
restaurants, rec_id = agent.recommend_restaurants(
    query=query,
    use_preferences=True  # Uses learned profile
)

# Provide rich feedback
agent.provide_feedback(
    recommendation_id=rec_id,
    restaurant_name=restaurants[0]['name'],
    liked=True,
    vibe_score=5,
    visited=True
)
```

### 6. **Q&A Prep** (Common Questions)

**Q: How does it learn preferences?**
A: "It tracks patterns in your feedback - if you consistently like Italian restaurants or 3-dollar places, it learns those preferences and boosts similar restaurants in future recommendations."

**Q: What makes this different from Google Maps?**
A: "Three things: (1) It learns YOUR specific taste, (2) Natural language queries, (3) Preference-aware ranking that improves over time."

**Q: What about API costs?**
A: "Very minimal - about $0.10 for 60 restaurants. Google gives $200 monthly free credit."

**Q: Can it handle multiple users?**
A: "Currently single-user, but the architecture supports multi-user - just add user IDs to the database schema."

**Q: How accurate is it?**
A: "It uses semantic search with embeddings, so it understands context beyond keywords. Plus, preference learning means it gets smarter with every interaction."

## 🚀 Quick Demo Alternative

If time is limited (2-3 minutes):

```bash
python matere_d_demo.py quick
```

This shows just the recommendation flow for multiple queries without setup details.

## 💡 Presentation Tips

1. **Energy**: Show enthusiasm about AI that learns from you
2. **Relatable**: "We've all had bad restaurant recommendations..."
3. **Technical Depth**: Mention ChromaDB, embeddings, preference learning
4. **Visual**: The demo has emojis and clear output - let it shine
5. **Future Vision**: "Imagine this with photos, reservations, social sharing..."

## 🎬 Opening Line Suggestions

- "What if your restaurant app actually learned what YOU like?"
- "I built an AI sommelier that gets smarter every time you dine out"
- "Google knows what's popular, but mATEre d' knows what YOU love"

## 📊 Key Metrics to Highlight

- Natural language processing (no structured queries)
- Multi-dimensional feedback (5 different signals)
- Dual database architecture (catalog + preferences)
- Real-time API integration
- Confidence scores on learned preferences

---

## 🔨 Agent Tools (Functions/Methods)

The mATEre d' agent exposes these tools/methods:

### 1. `fetch_and_store_restaurants`
**Purpose**: Fetch restaurants from Google Places API and store in vector database

**Parameters**:
- `location` (str): Street address, intersection, landmark, or subway station
  - Examples: "5th Ave and 42nd St", "Grand Central Terminal"
- `radius_meters` (int): Search radius in meters (default: 805m = 0.5 miles)
- `limit` (int): Maximum number of restaurants to fetch (default: 50)
- `keyword` (str, optional): Filter keyword (e.g., "korean bbq", "pizza")

**Returns**: Number of restaurants added to catalog

**Example**:
```python
count = agent.fetch_and_store_restaurants(
    location="Times Square",
    radius_meters=805,
    limit=60,
    keyword="korean bbq"
)
```

---

### 2. `recommend_restaurants`
**Purpose**: Get personalized restaurant recommendations using semantic search

**Parameters**:
- `query` (str): Natural language query
  - Examples: "romantic Italian", "cheap pizza", "korean bbq"
- `n_results` (int): Number of results to return (default: 5)
- `use_preferences` (bool): Apply learned preferences (default: True)

**Returns**: Tuple of (restaurants list, recommendation_id)

**Features**:
- Semantic search using ChromaDB embeddings
- Cuisine-aware keyword filtering
- Price range filtering ("cheap" → $, "expensive" → $$$)
- Preference boosting based on past feedback

**Example**:
```python
restaurants, rec_id = agent.recommend_restaurants(
    query="cheap pizza",
    n_results=2,
    use_preferences=True
)
```

---

### 3. `provide_feedback`
**Purpose**: Record user feedback to learn preferences

**Parameters**:
- `recommendation_id` (str): ID from recommend_restaurants
- `restaurant_name` (str): Name of the restaurant
- `liked` (bool, optional): Whether user liked it
- `vibe_score` (int, optional): Score from 1-5
- `fits_query` (bool, optional): Did it match the query?
- `visited` (bool, optional): Did user visit it?
- `notes` (str, optional): Free-form feedback

**Returns**: None (updates preference database)

**Example**:
```python
agent.provide_feedback(
    recommendation_id=rec_id,
    restaurant_name="KPOT Korean BBQ",
    liked=True,
    vibe_score=5,
    fits_query=True,
    visited=True,
    notes="Amazing atmosphere!"
)
```

---

### 4. `show_learned_preferences`
**Purpose**: Display learned cuisine and price preferences

**Parameters**: None

**Returns**: None (prints to console)

**Output Example**:
```
📊 Cuisine Preferences:
  Korean: 3 likes, 0 dislikes (confidence: 100.0%)
  Italian: 2 likes, 0 dislikes (confidence: 100.0%)

💰 Price Range Preferences:
  $$: 3 likes (confidence: 60.0%)
  $: 2 likes (confidence: 40.0%)
```

---

### 5. `show_statistics`
**Purpose**: Display feedback and recommendation statistics

**Parameters**: None

**Returns**: None (prints to console)

**Output Example**:
```
📈 Feedback Statistics:
  Total Feedback: 5
  Liked: 4
  Disliked: 1
  Visited: 3

🎯 Recommendation Statistics:
  Total Recommendations: 10
```

---

## 🔄 Tool Workflow

```
1. fetch_and_store_restaurants()
   ↓
   [Builds restaurant catalog in ChromaDB]
   ↓
2. recommend_restaurants()
   ↓
   [Returns personalized recommendations]
   ↓
3. provide_feedback()
   ↓
   [Updates preference database]
   ↓
4. show_learned_preferences()
   [View learned patterns]
```

---

## 🛠️ Tools & Technologies Used

### External APIs
1. **Google Places API (Nearby Search)**
   - Purpose: Fetch real-time restaurant data
   - Features: Location-based search, keyword filtering, radius-based results
   - Endpoints: Geocoding API + Places Nearby Search
   - Cost: ~$0.10 per 60 restaurants (free tier: $200/month)

2. **Google Geocoding API**
   - Purpose: Convert addresses/landmarks to coordinates
   - Examples: "Times Square" → lat/lng, "5th Ave & 42nd St" → coordinates
   - Enables: NYC-only mode, flexible location inputs

### Vector Database
3. **ChromaDB**
   - Purpose: Semantic search and restaurant catalog
   - Features:
     - Embedding-based similarity search
     - Persistent storage
     - Efficient restaurant matching
   - Why: Enables natural language queries beyond keyword matching

### Data Storage
4. **SQLite**
   - Purpose: User preferences and feedback tracking
   - Tables:
     - `user_preferences`: Learned cuisine/price preferences
     - `feedback`: Restaurant ratings, vibe scores, notes
     - `recommendations`: Recommendation history
   - Why: Lightweight, serverless, perfect for single-user agents

### Natural Language Processing
5. **Sentence Transformers / Embeddings**
   - Purpose: Convert restaurant descriptions to vectors
   - Features:
     - 150+ dish-specific keywords
     - Cuisine-aware embeddings
     - Price semantics ("cheap" → "$", "expensive" → "$$$")
   - Enables: "korean bbq" matching actual Korean BBQ restaurants

### Python Libraries
6. **requests**
   - Purpose: HTTP calls to Google APIs
   - Usage: Geocoding, Places search

7. **uuid**
   - Purpose: Generate unique recommendation IDs
   - Usage: Track feedback for specific recommendations

8. **datetime**
   - Purpose: Timestamp feedback and preferences
   - Usage: Track when restaurants were tried

### Architecture Pattern
9. **Dual Database Design**
   - **ChromaDB**: Restaurant catalog (ephemeral, rebuilt per search)
   - **SQLite**: User preferences (persistent, grows over time)
   - Why: Separates transient search data from long-term learning

10. **Preference Learning System**
    - Algorithm: Tracks cuisine/price patterns from feedback
    - Boosting: Increases match scores for preferred types
    - Confidence: Calculates certainty based on feedback count

---

## 🔧 Technical Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Restaurant Data | Google Places API | Real-time restaurant info |
| Location Search | Google Geocoding API | Address → Coordinates |
| Semantic Search | ChromaDB + Embeddings | Natural language matching |
| Preference Storage | SQLite | Learning user taste |
| Query Processing | Keyword Detection | Price/cuisine filtering |
| Feedback System | Multi-dimensional tracking | Vibe, visited, notes |

---

## 💡 Why These Tools?

**Google Places API**: Most accurate, up-to-date restaurant data
**ChromaDB**: Better than keyword search - understands "noodles" = ramen/pho/lo mein
**SQLite**: Simple, portable, no server needed
**Embeddings**: Enables "korean bbq" to match restaurants with Korean cuisine
**Dual DBs**: Keeps catalog fresh while preserving learned preferences

---

**Good luck with your presentation! 🍷**
