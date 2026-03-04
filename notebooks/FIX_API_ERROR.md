# 🔧 Quick Fix: REQUEST_DENIED Error

## The Error You're Seeing

```
❌ Google Places API Error: REQUEST_DENIED
⚠️  API error: REQUEST_DENIED
✅ Added 0 restaurants to catalog
```

## Why This Happens

Your Google Places API is not set up correctly. One of these is the issue:
1. ❌ Places API not enabled in Google Cloud
2. ❌ Billing not set up
3. ❌ Wrong API key in `.env` file
4. ❌ API key doesn't have permissions

---

## ⚡ Quick Fix (5 minutes)

### 1. Check Your API Key
```bash
cat .env
```
Should show:
```
GOOGLE_PLACES_API_KEY=AIzaSyC...something...
```

If empty or wrong, update it.

### 2. Enable Places API
1. Go to: **https://console.cloud.google.com/apis/library**
2. Search: **"Places API"**
3. Click it and press **"Enable"**

### 3. Set Up Billing
1. Go to: **https://console.cloud.google.com/billing**
2. Click **"Link a billing account"**
3. Add credit card

**Don't worry:** $200 free credit per month, demo costs ~$0.10

### 4. Test It Works
```bash
python test_google_api.py
```

Should see:
```
✅ API is working! Found 20 restaurants
```

---

## 📖 Detailed Setup

See **GOOGLE_API_SETUP.md** for complete step-by-step instructions.

---

## ✅ Once Fixed

Run the demo:
```bash
python matere_d_demo.py
```

Now you can input your own query when prompted!

---

## 🆘 Still Stuck?

1. Try creating a **new API key** in Google Cloud Console
2. Make sure you're using a **personal Gmail account** (not school/work)
3. Double-check **Places API** (not "Places API (New)") is enabled
4. Check **GOOGLE_API_SETUP.md** for troubleshooting

---

**The API setup is the only blocker. Once that's done, everything will work! 🍷**
