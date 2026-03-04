# 🎯 Match Score Explained

## What is the Match Score?

The **Match Score** is a percentage (0-100%) that shows how well a restaurant matches your query and preferences.

```
Match Score: 87.3%  ← This means 87.3% match
```

---

## How It's Calculated

### Step 1: Semantic Similarity (Base Score)

When you search for "romantic Italian restaurant for date night", mATEre d':

1. **Converts your query to an embedding** (vector representation)
2. **Compares it to all restaurant embeddings** in the database
3. **Calculates similarity** using ChromaDB's distance metric

**ChromaDB Distance:**
- `0.0` = Perfect match (identical)
- `0.3` = Very similar
- `0.7` = Somewhat similar
- `1.5+` = Not very similar

**Converted to Percentage:**
```python
similarity = max(0, 1 - distance)  # Distance → Similarity (0 to 1)
base_score = similarity * 100       # Convert to percentage (0-100%)
```

**Example:**
- Distance = 0.3 → Similarity = 0.7 → **Base Score = 70%**
- Distance = 0.5 → Similarity = 0.5 → **Base Score = 50%**
- Distance = 0.1 → Similarity = 0.9 → **Base Score = 90%**

---

### Step 2: Preference Boosting (Learned Preferences)

If you've provided feedback, mATEre d' **boosts scores** for restaurants matching your preferences:

**Cuisine Boost:**
```
If you previously liked Italian restaurants:
  Confidence = 80% (you liked Italian 4 out of 5 times)
  Boost = +16% (0.8 confidence × 0.2 boost factor × 100)
```

**Price Boost:**
```
If you prefer $$$ restaurants:
  Confidence = 60%
  Boost = +6% (0.6 confidence × 0.1 boost factor × 100)
```

**Final Score:**
```
Match Score = Base Score + Cuisine Boost + Price Boost
            = 70% + 16% + 6%
            = 92%
```

---

## Understanding Your Scores

### 🟢 High Match (70-100%)
- Restaurant strongly matches your query
- May have cuisine/price you've liked before
- **Recommended:** Very likely you'll enjoy it

### 🟡 Medium Match (40-70%)
- Decent match but not perfect
- Might be missing some aspects of your query
- **Maybe:** Worth considering if limited options

### 🔴 Low Match (0-40%)
- Weak match to your query
- Different from your usual preferences
- **Skip:** Probably not what you're looking for

---

## Why Scores Change Over Time

As you provide more feedback, the system learns:

**First Search (No Feedback Yet):**
```
Query: "romantic Italian restaurant"
Result: Carbone - Base Score: 75%
```

**After Liking Italian Places:**
```
Query: "romantic Italian restaurant"
Result: Carbone - Base: 75% + Italian Boost: +15% = 90%
                  ↑ Same restaurant, higher score!
```

The algorithm learns you like Italian → boosts Italian restaurants in future searches.

---

## Example Breakdown

### Query: "cheap Mexican food"

**Restaurant A: Taco Bell**
```
Base similarity: 65%
  ↳ "Mexican", "cheap", "food" all match

Cuisine boost: +12%
  ↳ You liked Mexican before (confidence: 60%)

Price boost: +8%
  ↳ You prefer $ restaurants (confidence: 80%)

Final Score: 65% + 12% + 8% = 85% ✅
```

**Restaurant B: Per Se (French fine dining)**
```
Base similarity: 20%
  ↳ Only "food" matches, wrong cuisine, wrong price

Cuisine boost: 0%
  ↳ You don't prefer French

Price boost: 0%
  ↳ You don't prefer $$$$

Final Score: 20% + 0% + 0% = 20% ❌
```

---

## Technical Details

### Why Use Embeddings?

Traditional keyword search:
```
Query: "romantic Italian date night"
Match: Restaurant must contain words "romantic", "Italian", etc.
```

Semantic embeddings:
```
Query: "romantic Italian date night"
Match: Restaurants with similar MEANING, even with different words
  ✅ "Intimate Tuscan dining experience"
  ✅ "Cozy trattoria perfect for couples"
  ✅ "Candlelit Italian bistro"
```

Embeddings capture meaning, not just words!

### The Math (For Nerds 🤓)

```python
# ChromaDB uses cosine distance
distance = 1 - cosine_similarity(query_embedding, restaurant_embedding)

# We convert to similarity percentage
similarity = max(0, 1 - distance)
base_score = similarity * 100

# Add preference boosts
if cuisine matches learned preference:
    score += preference_confidence * 20  # Max +20%

if price matches learned preference:
    score += preference_confidence * 10  # Max +10%

# Cap at 100%
final_score = min(100, score)
```

---

## Summary

**Match Score = How well the restaurant fits your query + your past preferences**

- **70-100%**: Great match, go for it! 🎯
- **40-70%**: Decent option, might work
- **0-40%**: Probably not what you want

The more feedback you provide, the smarter the scores become! 🧠

---

**Now you understand the magic behind the numbers! ✨**
