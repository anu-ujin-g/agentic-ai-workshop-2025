# 🔧 FIX: Geocoding API Error

## The Error You're Seeing

```
❌ Could not find location: times square
   Status: REQUEST_DENIED
   Error: This API project is not authorized to use this API.
```

## What This Means

You have **Places API** enabled, but you're missing **Geocoding API**.

mATEre d' uses **TWO Google APIs**:
1. ✅ Places API - for finding restaurants (you have this)
2. ❌ Geocoding API - for converting location → coordinates (you need this!)

---

## Quick Fix (2 minutes)

### Step 1: Enable Geocoding API

1. Go to: **https://console.cloud.google.com/apis/library**
2. Search for: **"Geocoding API"**
3. Click on **"Geocoding API"**
4. Click **"Enable"**

### Step 2: Wait 1-2 Minutes

Sometimes takes a moment to activate.

### Step 3: Try Again

```bash
python matere_d_demo.py
```

You should now see:
```
✓ Found: Times Square, Manhattan, NY 10036, USA
```

---

## Why You Need Both APIs

### Geocoding API
**Purpose:** Convert location text → coordinates

**Example:**
```
Input:  "Times Square"
Output: 40.758896, -73.985130
```

**Used for:** Understanding where you are

### Places API
**Purpose:** Find restaurants near coordinates

**Example:**
```
Input:  40.758896, -73.985130 (radius: 805m)
Output: [List of 60 restaurants]
```

**Used for:** Finding restaurants

### Together
```
Your input: "Times Square"
    ↓
Geocoding API: "Times Square" → 40.758, -73.985
    ↓
Places API: Find restaurants within 0.5 miles of 40.758, -73.985
    ↓
Results: 60 restaurants near Times Square
```

---

## Visual Guide

### 1. Go to API Library

```
https://console.cloud.google.com/apis/library
```

### 2. Search "Geocoding API"

<img width="400" alt="Search box with 'Geocoding API'">

### 3. Click "Geocoding API"

You'll see:
```
Geocoding API
Convert addresses to coordinates and vice versa
```

### 4. Click "Enable"

<img width="200" alt="Blue Enable button">

### 5. Done!

You'll see:
```
API enabled
✓ Geocoding API is now enabled
```

---

## Cost

**Geocoding API Pricing:**
- $5 per 1,000 requests
- mATEre d' uses: 1 request per demo run
- **Cost per run: $0.005 (half a cent!)**

**With Free Tier:**
- $200 monthly credit
- Can run ~40,000 times before paying anything!

---

## Still Not Working?

### Check Both APIs Are Enabled

1. Go to: **https://console.cloud.google.com/apis/dashboard**
2. You should see BOTH:
   - ✅ **Geocoding API**
   - ✅ **Places API**

### Make Sure Same Project

Both APIs must be enabled in the **same Google Cloud project** that your API key is from.

**Check:**
1. Top of Google Cloud Console shows project name
2. Both APIs should be in this project

### Try New API Key

If still failing:
1. Go to: **https://console.cloud.google.com/apis/credentials**
2. Delete old API key
3. Click **"+ CREATE CREDENTIALS"** → **"API key"**
4. Copy new key
5. Update `.env` file:
   ```
   GOOGLE_PLACES_API_KEY=your_new_key_here
   ```

---

## Test It Works

```bash
# Test geocoding specifically
python -c "
import os, requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_PLACES_API_KEY')

response = requests.get(
    'https://maps.googleapis.com/maps/api/geocode/json',
    params={'address': 'Times Square, New York', 'key': api_key}
)
data = response.json()

if data['status'] == 'OK':
    print('✅ Geocoding API is working!')
    print(f\"Found: {data['results'][0]['formatted_address']}\")
else:
    print(f\"❌ Error: {data['status']}\")
    if 'error_message' in data:
        print(f\"   {data['error_message']}\")
"
```

**Expected output:**
```
✅ Geocoding API is working!
Found: Times Square, Manhattan, NY 10036, USA
```

---

## Checklist

- [ ] Go to https://console.cloud.google.com/apis/library
- [ ] Search "Geocoding API"
- [ ] Click "Enable"
- [ ] Wait 1-2 minutes
- [ ] Run `python matere_d_demo.py`
- [ ] See "✓ Found: [location]"

---

## Summary

**Problem:** Geocoding API not enabled
**Solution:** Enable it in Google Cloud Console
**Time:** 2 minutes
**Cost:** $0.005 per run (~half a cent)

**Once enabled, location input will work perfectly!**

---

**Enable Geocoding API now:** https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com
