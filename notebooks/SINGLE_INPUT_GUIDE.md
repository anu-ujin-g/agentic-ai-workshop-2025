# 🔍 Single Input - Search Made Simple!

## One Input for Everything

No more separate location and query! Just type what you want in **one line**.

---

## Format

```
[what you want] [location keyword] [where you are]
```

**Location keywords:** `near`, `at`, `around`, `by`, `in`

---

## Examples

### ✅ Perfect Format

```
cheap pizza near Times Square
romantic Italian at Grand Central
quick lunch around Penn Station
sushi by 5th Ave and 42nd St
tacos in SoHo
burger near 350 5th Avenue
```

### How It Works

**Input:** `"cheap pizza near Times Square"`

**Extracts:**
- Query: `"cheap pizza"`
- Location: `"Times Square"`

**Then:**
1. Geocodes "Times Square" → coordinates
2. Finds restaurants within 0.5 miles
3. Searches for "cheap pizza"
4. Returns top 2 matches

---

## All Location Keywords

Use any of these to separate query from location:

| Keyword | Example |
|---------|---------|
| **near** | `sushi near Grand Central` |
| **at** | `brunch at Times Square` |
| **around** | `coffee around Penn Station` |
| **by** | `pizza by 5th Ave and 42nd St` |
| **in** | `tacos in Greenwich Village` |

---

## What You'll See

### Example 1: With Location Keyword

```
🔍 What are you looking for?
   Examples:
   • 'cheap pizza near Times Square'
   • 'romantic Italian restaurant at Grand Central'
   • 'quick lunch near 350 5th Ave'
   • 'sushi around Penn Station'

   Your search: cheap pizza near Times Square

Building catalog for Times Square...
✓ Found: Times Square, Manhattan, NY 10036, USA

Results for: "cheap pizza"

1. Joe's Pizza
   Italian • $ • ⭐ 4.5/5 (1234 reviews)
   Match: 85.3%
   7 Carmine St, New York, NY

2. Prince Street Pizza
   Italian • $ • ⭐ 4.6/5 (987 reviews)
   Match: 82.1%
   27 Prince St, New York, NY
```

### Example 2: Without Location Keyword

If you just type `"pizza"`:

```
   Your search: pizza

📍 Where? (e.g., 'Times Square', '5th Ave & 42nd St'): Grand Central

Building catalog for Grand Central...
✓ Found: Grand Central Terminal, New York, NY 10017, USA

Results for: "pizza"
...
```

---

## Real-World Examples

### Quick Lunch at Work

```
Your search: quick lunch near 350 5th Avenue
```

### Date Night

```
Your search: romantic Italian at SoHo
```

### Tourist at Landmark

```
Your search: cheap food near Statue of Liberty
```

### Near Subway Station

```
Your search: coffee around Union Square Station
```

### In Neighborhood

```
Your search: brunch in Williamsburg Brooklyn
```

### Street Intersection

```
Your search: sushi by 5th Ave and 42nd St
```

---

## Tips

### ✅ DO Use Location Keywords

**Good:**
```
pizza near Times Square
sushi at Grand Central
tacos in SoHo
```

### ❌ DON'T Forget Location Keyword

**This won't auto-detect location:**
```
pizza Times Square  ← No keyword!
```

**Will ask you separately:**
```
📍 Where? (e.g., 'Times Square'): Times Square
```

### 💡 Be Natural

The system understands natural language:

```
✅ "I want cheap pizza near Times Square"
✅ "cheap pizza near Times Square"
✅ "pizza near Times Square"
```

All work! The location extraction is smart.

---

## Location Formats Supported

After the keyword, you can use:

### Landmarks
```
near Empire State Building
at Central Park
around Brooklyn Bridge
```

### Stations
```
near Grand Central Station
at Penn Station
around Union Square Station
```

### Addresses
```
near 350 5th Avenue
at 123 Broadway
```

### Intersections
```
near 5th Ave and 42nd St
at Broadway & 34th St
```

### Neighborhoods
```
in SoHo
in Greenwich Village
in Williamsburg Brooklyn
```

---

## Complete Flow

```
======================================================================
🍷  mATEre d' - Your AI Restaurant Sommelier  🍷
======================================================================
An intelligent agent that learns your dining preferences over time
======================================================================

🔍 What are you looking for?
   Examples:
   • 'cheap pizza near Times Square'
   • 'romantic Italian restaurant at Grand Central'
   • 'quick lunch near 350 5th Ave'
   • 'sushi around Penn Station'

   Your search: romantic Italian near Grand Central

Building catalog for Grand Central...
✓ Found: Grand Central Terminal, New York, NY 10017, USA

Results for: "romantic Italian"

1. Carbone
   Italian • $$$ • ⭐ 4.7/5 (2341 reviews)
   Match: 92.5%
   181 Thompson St, New York, NY

2. L'Artusi
   Italian • $$$ • ⭐ 4.6/5 (1823 reviews)
   Match: 88.3%
   228 W 10th St, New York, NY

Would you like to provide feedback? (y/n): n
```

---

## Summary

**Old way (2 inputs):**
```
📍 Location: Times Square
🔍 Query: cheap pizza
```

**New way (1 input):**
```
🔍 Your search: cheap pizza near Times Square
```

**Much simpler!** 🎯

---

## Quick Reference

**Format:** `[what] [keyword] [where]`

**Keywords:** `near`, `at`, `around`, `by`, `in`

**Example:** `cheap pizza near Times Square`

**Done!** 🍷
