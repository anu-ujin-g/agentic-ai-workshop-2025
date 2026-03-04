# 🔧 mATEre d' - Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: IndexError - list index out of range

**Error:**
```
IndexError: list index out of range
```

**Cause:** The restaurant catalog is empty, so no recommendations can be returned.

**Solution:**
1. Make sure you're running the demo for the first time (it will populate the catalog)
2. Or manually populate the catalog:
   ```python
   from pathlib import Path
   from matere_d_agent import SmartRestaurantAgent
   import os
   from dotenv import load_dotenv

   load_dotenv()
   agent = SmartRestaurantAgent(
       google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
       data_dir=Path('data/matere_d')
   )
   agent.fetch_and_store_restaurants(location="New York, NY", limit=60)
   ```

---

### Issue 2: Google API Key Not Found

**Error:**
```
GOOGLE_PLACES_API_KEY not found in .env file!
```

**Solution:**
1. Create a `.env` file in the `notebooks/` directory
2. Add your API key:
   ```
   GOOGLE_PLACES_API_KEY=your_actual_api_key_here
   ```
3. Get an API key from [Google Cloud Console](https://console.cloud.google.com/)

---

### Issue 3: REQUEST_DENIED from Google API

**Error:**
```
API status: REQUEST_DENIED
```

**Common Causes:**
1. **API key is invalid** - Double-check your key in `.env`
2. **Places API not enabled** - Enable "Places API" in Google Cloud Console
3. **Billing not set up** - Google requires a billing account (has free tier)
4. **API restrictions** - Check if your API key has IP/application restrictions

**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable "Places API" for your project
3. Set up billing (you get $200 free credit/month)
4. Create or regenerate API key
5. Update your `.env` file

---

### Issue 4: No Restaurants Found

**Symptom:**
```
⚠️  No restaurants found!
```

**Solutions:**
1. **Check catalog size:**
   ```bash
   python test_matere_d.py
   ```
   Look for "X restaurants in catalog"

2. **Re-populate catalog:**
   ```bash
   rm -rf data/matere_d/
   python matere_d_demo.py
   ```

3. **Try different location:**
   Edit `matere_d_demo.py` and change location:
   ```python
   agent.fetch_and_store_restaurants(location="San Francisco, CA", limit=60)
   ```

---

### Issue 5: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'chromadb'
```

**Solution:**
```bash
pip install chromadb requests python-dotenv
```

If using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install chromadb requests python-dotenv
```

---

### Issue 6: Slow API Responses

**Symptom:** Demo takes a long time to fetch restaurants

**Cause:** Google API can be slow, especially with pagination

**Solutions:**
1. **Reduce restaurant limit:**
   ```python
   agent.fetch_and_store_restaurants(location="New York, NY", limit=20)  # Instead of 60
   ```

2. **Use cached data:** Once populated, the catalog persists in `data/matere_d/`

3. **Check internet connection**

---

### Issue 7: Preferences Not Learning

**Symptom:** Learned preferences are empty or not updating

**Possible Causes:**
1. Haven't provided enough feedback yet
2. Database not writing properly
3. Confidence scores too low

**Solutions:**
1. **Provide more feedback:** System needs at least 2-3 feedback entries
2. **Check database:**
   ```bash
   ls -la data/matere_d/user_preferences/user_preferences.db
   ```
3. **Lower confidence threshold:** Edit `matere_d_preferences.py:264`:
   ```python
   WHERE confidence > 0.2  # Instead of 0.3
   ```

---

## Testing Checklist

Run before your presentation:

```bash
# 1. Test everything works
python test_matere_d.py

# 2. Test Google API directly
python test_google_api.py

# 3. Run the demo once
python matere_d_demo.py

# 4. If successful, delete data for fresh demo
rm -rf data/matere_d/
```

---

## Getting Help

### Debug Mode

Add debug output to see what's happening:

```python
# In matere_d_agent.py, add after line 135:
print(f"DEBUG: Query returned {len(results['ids'][0])} results")
print(f"DEBUG: First result: {results['metadatas'][0][0] if results['metadatas'][0] else 'None'}")
```

### Check Data

```python
# Check catalog size
from matere_d_agent import SmartRestaurantAgent
from pathlib import Path
import os

agent = SmartRestaurantAgent(
    google_api_key=os.getenv('GOOGLE_PLACES_API_KEY'),
    data_dir=Path('data/matere_d')
)
print(f"Catalog size: {agent.restaurant_collection.count()}")
```

### Logs

Check for error logs:
```bash
python matere_d_demo.py 2>&1 | tee demo_log.txt
```

---

## Emergency Fixes

### Nuclear Option - Complete Reset

If nothing works, start fresh:

```bash
# 1. Delete all data
rm -rf data/matere_d/
rm -rf data/matere_d_test/

# 2. Verify .env file
cat .env | grep GOOGLE_PLACES_API_KEY

# 3. Test API manually
python test_google_api.py

# 4. Re-run demo
python matere_d_demo.py
```

---

## API Cost Monitoring

Check your Google Cloud Console:
- [APIs & Services > Dashboard](https://console.cloud.google.com/apis/dashboard)
- Look for "Places API" usage
- ~60 restaurants = 3-4 API calls = ~$0.10

---

Need more help? Check the logs above or contact support.
