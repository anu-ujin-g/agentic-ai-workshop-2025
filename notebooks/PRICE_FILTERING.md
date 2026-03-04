# 💰 Price Range Filtering

## How It Works

You can now use natural language to filter restaurants by price range!

---

## Price Keywords

### Cheap / Budget ($)
**Keywords:**
- cheap
- inexpensive
- budget
- affordable
- value

**Example Results:** $1.50 Fresh Pizza • $ • ⭐ 4.5/5

---

### Moderate / Mid-Range ($$)
**Keywords:**
- moderate
- mid-range
- medium

**Example Results:** K-Bap & Wings • $$ • ⭐ 4.7/5

---

### Expensive / Upscale ($$$)
**Keywords:**
- expensive
- fancy
- upscale
- fine dining
- luxury
- pricey

**Example Results:** Chazz Palminteri Italian Restaurant • $$$ • ⭐ 4.6/5

---

## Example Searches

### Budget-Friendly
```
What are you craving? cheap pizza near times square

1. $1.50 Fresh Pizza
   Italian • $ • ⭐ 4.5/5 (2569 reviews)
   Match: 100.8%
   143 W 40th St, New York

2. $1.50 Fresh Pizza
   Italian • $ • ⭐ 4.5/5 (2415 reviews)
   Match: 99.4%
   151 E 43rd St, New York
```

### Affordable Sushi
```
What are you craving? affordable sushi near times square

1. Teriyaki One Japanese Grill (Teriyaki & Sushi)
   Japanese • $ • ⭐ 4.6/5 (280 reviews)
   Match: 25.0%
   42 W 56th St, New York

2. Happy Tuna Sushi & Crispy Rice
   Japanese • $ • ⭐ 4.7/5 (315 reviews)
   Match: 25.0%
   355 W 36th St, New York
```

### Mid-Range Korean
```
What are you craving? moderate korean near times square

1. K-Bap & Wings | Korean
   Korean • $$ • ⭐ 4.7/5 (1404 reviews)
   Match: 30.0%
   62 W 56th St, New York
```

### Fancy Italian
```
What are you craving? expensive italian near times square

1. Chazz Palminteri Italian Restaurant
   Italian • $$$ • ⭐ 4.6/5 (1452 reviews)
   Match: 36.0%
   30 W 46th St, New York
```

---

## Combining Filters

You can combine price with cuisine and location:

```
cheap pizza near times square         → Italian, $
affordable sushi around grand central → Japanese, $
moderate korean at 5th and 42nd      → Korean, $$
expensive italian in midtown         → Italian, $$$
fancy french near broadway           → French, $$$
budget-friendly mexican near penn    → Mexican, $
```

---

## How Filtering Works

1. **Detects price keywords** in your query
2. **Maps to price range**:
   - cheap/affordable → $
   - moderate → $$
   - expensive/fancy → $$$
3. **Filters restaurants** to match that price range
4. **Boosts match score** for restaurants in the desired price range (+10%)

---

## Price Range Legend

| Symbol | Meaning | Typical Cost per Person |
|--------|---------|------------------------|
| $ | Inexpensive | Under $15 |
| $$ | Moderate | $15-30 |
| $$$ | Expensive | $30-60 |
| $$$$ | Very Expensive | Over $60 |

Note: Most restaurants in Google Places are $-$$$.

---

## Tips

1. **Be specific**: "cheap pizza" works better than just "pizza"
2. **Mix criteria**: "affordable korean bbq near times square"
3. **Use synonyms**: "budget", "inexpensive", "value" all work
4. **Try variations**: "fancy", "upscale", "fine dining" for expensive

---

## All Supported Keywords

### Cheap ($)
- cheap
- inexpensive
- budget
- affordable
- value

### Moderate ($$)
- moderate
- mid-range
- medium

### Expensive ($$$)
- expensive
- fancy
- upscale
- fine dining
- luxury
- pricey

---

## Examples in Action

```bash
python matere_d_demo.py
```

Try these:
1. "cheap noodles near times square"
2. "fancy sushi at grand central"
3. "affordable korean bbq near broadway"
4. "expensive steakhouse in midtown"
5. "budget pizza near penn station"

Enjoy finding restaurants that match your budget! 💰
