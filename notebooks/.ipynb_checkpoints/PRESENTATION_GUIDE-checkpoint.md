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

**Good luck with your presentation! 🍷**
