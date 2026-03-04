# 🔑 Google Places API Setup Guide

## The Problem

You're seeing: **❌ API error: REQUEST_DENIED**

This means Google is rejecting your API request. Let's fix it!

---

## ✅ Step-by-Step Setup (5 minutes)

### Step 1: Go to Google Cloud Console
👉 **https://console.cloud.google.com/**

### Step 2: Create or Select a Project
1. Click the project dropdown at the top
2. Click "New Project" or select an existing one
3. Give it a name (e.g., "mATEre-d-restaurant-agent")

### Step 3: Enable TWO APIs (Both Required!)

**You need to enable BOTH of these:**

#### 3a. Enable Places API
1. Go to **APIs & Services > Library**
   - Or direct link: https://console.cloud.google.com/apis/library
2. Search for **"Places API"**
3. Click on **"Places API"** (not "Places API (New)")
4. Click **"Enable"**

#### 3b. Enable Geocoding API
1. In the same **APIs & Services > Library** page
2. Search for **"Geocoding API"**
3. Click on **"Geocoding API"**
4. Click **"Enable"**

**Why you need both:**
- **Places API** - Finds restaurants near a location
- **Geocoding API** - Converts "Times Square" → coordinates

### Step 4: Set Up Billing
1. Go to **Billing** in the left menu
   - Or direct link: https://console.cloud.google.com/billing
2. Click **"Link a billing account"**
3. Add a credit card (required even for free tier)

**Don't worry about cost:**
- Google gives $200 free credit per month
- Places API costs ~$32 per 1,000 requests
- Our demo uses ~3-4 requests (~$0.10)
- You'll get alerts if you approach limits

### Step 5: Create API Key
1. Go to **APIs & Services > Credentials**
   - Or direct link: https://console.cloud.google.com/apis/credentials
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"API key"**
4. Copy the key (starts with `AIza...`)

### Step 6: Configure Your Project
1. Create or edit `.env` file in the `notebooks/` directory:
   ```bash
   GOOGLE_PLACES_API_KEY=AIzaSyC-your-actual-key-here
   ```

2. **Important:** Replace `AIzaSyC-your-actual-key-here` with your actual key!

---

## 🧪 Test Your Setup

```bash
python test_google_api.py
```

You should see:
```
✅ API key found: AIzaSyC...
🌐 Testing Google Places API...
Status: OK
✅ API is working! Found 20 restaurants
```

---

## 🚨 Common Issues

### Issue 1: Still Getting REQUEST_DENIED

**Check these:**

1. **Is Places API enabled?**
   ```
   Go to: APIs & Services > Dashboard
   You should see "Places API" in the list
   ```

2. **Is billing set up?**
   ```
   Go to: Billing
   Should show active billing account
   ```

3. **Is the API key correct in .env?**
   ```bash
   cat .env | grep GOOGLE_PLACES_API_KEY
   ```

4. **Try creating a new API key:**
   - Sometimes old keys don't work
   - Delete old key, create new one
   - Update `.env` file

### Issue 2: OVER_QUERY_LIMIT

**Cause:** You've exceeded the free tier

**Solution:**
- Check usage in Google Cloud Console
- Set up billing alerts
- Wait until next month for reset

### Issue 3: INVALID_REQUEST

**Cause:** API request format is wrong

**Solution:**
- This shouldn't happen with our code
- Check if you modified `matere_d_agent.py`

---

## 💰 Cost Calculator

| Action | API Calls | Cost |
|--------|-----------|------|
| Fetch 60 restaurants | 3-4 | ~$0.10 |
| Run demo 10 times | 30-40 | ~$1.00 |
| Monthly free credit | - | $200 |

**You can run the demo ~2,000 times before paying anything!**

---

## 🔒 Security Tips

1. **Never commit .env file to git:**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Restrict your API key (optional but recommended):**
   - Go to API key settings in Google Cloud Console
   - Add application restrictions (HTTP referrers or IP addresses)
   - Add API restrictions (only allow Places API)

3. **Set up budget alerts:**
   - Go to Billing > Budgets & alerts
   - Set alert at $10 to get notified

---

## ✅ Verification Checklist

Before running the demo:

- [ ] Created Google Cloud Project
- [ ] Enabled "Places API"
- [ ] Set up billing (credit card added)
- [ ] Created API key
- [ ] Added key to `.env` file
- [ ] Ran `python test_google_api.py` successfully

---

## 🆘 Still Not Working?

### Double-check everything:

```bash
# 1. Check .env file exists and has key
cat .env

# 2. Test the API directly
python test_google_api.py

# 3. Check Google Cloud Console
# Go to: APIs & Services > Dashboard
# Should show "Places API" with requests

# 4. Try a fresh API key
# Delete old key, create new one, update .env
```

### Last Resort - Use a Different Google Account

Sometimes corporate/school Google accounts have restrictions:
1. Create a personal Gmail account
2. Set up new Google Cloud project
3. Follow steps above

---

## 📚 Official Documentation

- [Places API Overview](https://developers.google.com/maps/documentation/places/web-service/overview)
- [Get API Key](https://developers.google.com/maps/documentation/places/web-service/get-api-key)
- [Billing Setup](https://cloud.google.com/billing/docs/how-to/manage-billing-account)

---

## ✨ Once It's Working

Run the demo:
```bash
python matere_d_demo.py
```

You should see:
```
🌐 Fetching restaurants from Google Places API...
✅ Added 60 restaurants to catalog
```

**Congratulations! You're ready to use mATEre d'! 🍷**
