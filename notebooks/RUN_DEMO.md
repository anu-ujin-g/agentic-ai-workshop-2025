# 🚀 Quick Start - Running mATEre d' Demo

## Prerequisites (5 minutes)

1. **Get Google Places API Key:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project or use existing
   - Enable "Places API"
   - Create API key
   - Set up billing (has free tier - $200/month credit)

2. **Create `.env` file:**
   ```bash
   echo "GOOGLE_PLACES_API_KEY=your_key_here" > .env
   ```

3. **Install dependencies:**
   ```bash
   pip install chromadb requests python-dotenv
   ```

---

## Test Setup (1 minute)

```bash
python test_matere_d.py
```

You should see:
- ✅ API key found
- ✅ All imports successful
- ✅ All dependencies installed
- ✅ Agent initialized
- ✅ API working! Test query found 20 restaurants
- 🎉 All tests passed!

---

## Run Demo (5-7 minutes)

### Option 1: Full Interactive Demo
```bash
python matere_d_demo.py
```

**What happens:**
1. Builds restaurant catalog (60 restaurants from Google Places)
2. Processes query: "romantic Italian restaurant for date night"
3. Shows top 3 recommendations with ratings, prices, addresses
4. Simulates feedback (liked, vibe score 5/5, visited)
5. Shows learned preferences
6. Shows usage statistics

### Option 2: Quick Demo (2-3 minutes)
```bash
python matere_d_demo.py quick
```

Shows just recommendations for multiple queries (requires existing catalog).

---

## Expected Output

```
======================================================================
🍷  mATEre d' - Your AI Restaurant Sommelier  🍷
======================================================================
An intelligent agent that learns your dining preferences over time
======================================================================

🔧 Initializing mATEre d'...
✅ Agent initialized!

──────────────────────────────────────────────────────────────────────
  STEP 1: Building Restaurant Catalog
──────────────────────────────────────────────────────────────────────

🌐 Fetching restaurants from Google Places API...
✨ Successfully cataloged 60 restaurants!

──────────────────────────────────────────────────────────────────────
  STEP 2: Getting Personalized Recommendations
──────────────────────────────────────────────────────────────────────

🔍 Your query: "romantic Italian restaurant for date night"

🧠 Analyzing preferences and searching...

🍽️  TOP RECOMMENDATIONS:

  1. Carbone
     └─ Italian Restaurant • $$$ • ⭐ 4.7/5 (2341 reviews)
     └─ Match Score: 87.3%
     └─ 181 Thompson St, New York, NY 10012

  2. L'Artusi
     └─ Italian Restaurant • $$$ • ⭐ 4.6/5 (1823 reviews)
     └─ Match Score: 85.2%
     └─ 228 W 10th St, New York, NY 10014

  3. Don Angie
     └─ Italian Restaurant • $$ • ⭐ 4.5/5 (1456 reviews)
     └─ Match Score: 82.1%
     └─ 103 Greenwich Ave, New York, NY 10014

... (continues with feedback, preferences, statistics)
```

---

## Troubleshooting

### Demo fails with IndexError?
**Cause:** Catalog is empty
**Fix:** Demo will auto-populate on first run. Wait for "Successfully cataloged X restaurants!"

### API returns REQUEST_DENIED?
**Cause:** API key issue or Places API not enabled
**Fix:**
1. Check `.env` file has correct key
2. Enable "Places API" in Google Cloud Console
3. Set up billing

### No restaurants found?
**Fix:**
```bash
rm -rf data/matere_d/
python matere_d_demo.py
```

**Full troubleshooting:** See `TROUBLESHOOTING.md`

---

## For Presentations

### Before You Present:
1. Run `python test_matere_d.py` to verify setup
2. Delete existing data for fresh demo: `rm -rf data/matere_d/`
3. Review `PRESENTATION_GUIDE.md` for talking points
4. Practice once to see timing

### During Presentation:
1. Show the command: `python matere_d_demo.py`
2. Let the demo run - it's self-explanatory with nice output
3. Highlight key features as they appear:
   - Google Places integration (Step 1)
   - Natural language query (Step 2)
   - Multi-dimensional feedback (Step 3)
   - Learned preferences (Step 4)
   - Statistics showing improvement (Step 5)

### Common Questions:
- **How does it learn?** - Tracks patterns in cuisine, price, ratings from feedback
- **Different from Google Maps?** - Learns YOUR taste, not just popularity
- **Cost?** - ~$0.10 for 60 restaurants, $200 free credit/month
- **Multi-user?** - Architecture supports it, just add user IDs

---

## Files Overview

```
📁 mATEre d' Project
├── matere_d_demo.py          ← Run this for demo
├── test_matere_d.py           ← Test setup first
├── test_google_api.py         ← Test API directly
│
├── matere_d_agent.py          ← Main agent
├── matere_d_preferences.py    ← Learning system
├── matere_d_google_places.py  ← API integration
│
├── RUN_DEMO.md                ← This file
├── PRESENTATION_GUIDE.md      ← Presentation tips
├── TROUBLESHOOTING.md         ← Debug help
└── MATERE_D_README.md         ← Full documentation
```

---

## Next Steps

1. ✅ Run `python test_matere_d.py`
2. ✅ Run `python matere_d_demo.py`
3. 📖 Read `PRESENTATION_GUIDE.md`
4. 🎤 Present with confidence!

**Good luck! 🍷**
