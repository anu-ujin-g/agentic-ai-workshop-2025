# 🆕 What's New - Latest Updates

## ✅ Three Major Improvements

### 1. 📍 Location-Based Search with 5-Minute Walk Radius

**What Changed:**
- Now asks for your specific location (street/avenue, intersection, address)
- Only searches within **400 meters** (~5-minute walk)
- Uses Google Geocoding + Nearby Search API for accurate radius filtering

**How to Use:**
```
📍 Where are you located?
   Examples:
   • 5th Avenue and 42nd Street
   • Times Square, New York
   • 350 5th Ave, New York, NY
   • 40.7580,-73.9855 (latitude,longitude)

📍 Your location: [TYPE HERE]
```

**Benefits:**
- ✅ Only shows restaurants you can actually walk to
- ✅ Supports street intersections, addresses, or lat/lng
- ✅ More practical for real-world use

---

### 2. 🎯 Fixed Match Scores (No More Negatives!)

**The Problem:**
Match scores were showing negative values like `-47.3%` 😵

**Why It Happened:**
- ChromaDB returns "distances" (lower = better)
- Old code: `match_score = 1 - distance`
- When distance > 1, this became negative!
- Preference boosts could make it worse

**The Fix:**
```python
# Now converts properly to 0-100% scale
similarity = max(0, 1 - distance)  # Ensure positive
match_score = similarity * 100     # Convert to percentage
match_score = min(100, max(0, match_score))  # Cap at 0-100%
```

**What You See Now:**
```
Match Score: 87.3%  ✅ (was: -47.3%)
Match Score: 65.2%  ✅ (was: -12.8%)
Match Score: 92.1%  ✅ (was: 108.4%)
```

**Explanation:**
See `MATCH_SCORE_EXPLAINED.md` for detailed breakdown of how scores work!

---

### 3. 🎲 Only 2 Recommendations (Not 5)

**What Changed:**
- Changed from showing 5 restaurants to just **top 2**
- Cleaner output, easier to decide
- Still records both for preference learning

**Before:**
```
🍽️  TOP RECOMMENDATIONS:
  1. Restaurant A
  2. Restaurant B
  3. Restaurant C
  4. Restaurant D
  5. Restaurant E
```

**After:**
```
🍽️  TOP 2 RECOMMENDATIONS:
  1. Restaurant A
  2. Restaurant B
```

**Why:**
- 🎯 Less overwhelming
- 🧠 Focus on best matches
- ⚡ Faster decision-making

---

## 📊 Match Score Breakdown

### Old System (Broken):
```
Distance from ChromaDB: 1.3
Match Score: 1 - 1.3 = -0.3 = -30% ❌
```

### New System (Fixed):
```
Distance from ChromaDB: 1.3
Similarity: max(0, 1 - 1.3) = 0
Base Score: 0 * 100 = 0%

With preference boost:
  + Italian cuisine boost: +16%
  + $$$ price boost: +6%

Final Score: 0% + 16% + 6% = 22% ✅
```

Even if base similarity is 0, preferences can still boost the score!

---

## 🗺️ Location Input Examples

All of these work:

```
✅ "Broadway and 42nd Street"
✅ "5th Ave and E 23rd St"
✅ "350 5th Avenue, New York, NY 10118"
✅ "Times Square"
✅ "40.758896,-73.985130"
✅ "Grand Central Terminal"
✅ "Central Park South"
```

The system will:
1. Geocode your input to get coordinates
2. Search for restaurants within 400m of that point
3. Store them in the catalog

---

## 🔧 API Requirements

**New APIs Used:**
1. **Geocoding API** - Convert address → lat/lng
2. **Places Nearby Search API** - Find restaurants within radius
   (Previously used: Text Search API)

**Make Sure These Are Enabled:**
1. Go to: https://console.cloud.google.com/apis/library
2. Enable:
   - ✅ Places API
   - ✅ Geocoding API

Both are included in the free tier!

---

## 📝 Updated Files

```
✅ matere_d_agent.py          - Location-based search, fixed scoring
✅ matere_d_demo.py            - Interactive location input, only 2 results
✅ MATCH_SCORE_EXPLAINED.md    - NEW: Complete scoring explanation
✅ WHATS_NEW.md                - NEW: This file
```

---

## 🚀 How to Use the New Features

### Step 1: Clear Old Data (Recommended)
```bash
rm -rf data/matere_d/
```

### Step 2: Run the Demo
```bash
python matere_d_demo.py
```

### Step 3: Enter Your Location
```
📍 Your location: Broadway and 42nd Street
```

### Step 4: Enter Your Query
```
🔍 Your query: cheap pizza place
```

### Step 5: See Your Results
```
🍽️  TOP 2 RECOMMENDATIONS:

  1. Joe's Pizza
     └─ Pizza Restaurant • $ • ⭐ 4.5/5 (1234 reviews)
     └─ Match Score: 78.3%
     └─ 150 Broadway, New York, NY
```

---

## 📚 Learn More

- **MATCH_SCORE_EXPLAINED.md** - How scoring works
- **GOOGLE_API_SETUP.md** - API setup guide
- **FIX_API_ERROR.md** - Troubleshooting
- **TROUBLESHOOTING.md** - General issues

---

## 🎉 Summary

Three simple improvements:
1. 📍 **Enter your location** → get walkable restaurants
2. 🎯 **Fixed scores** → 0-100% (no negatives!)
3. 🎲 **Only 2 results** → easier to choose

**Everything else works the same!**

---

**Try it now: `python matere_d_demo.py` 🍷**
