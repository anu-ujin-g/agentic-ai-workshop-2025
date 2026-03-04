# 🗽 NYC-Only Mode - Enabled!

## What Changed

The system now **automatically assumes all locations are in NYC**.

---

## How It Works

**You type:**
```
5th Ave and 42nd St
```

**System converts to:**
```
5th Ave and 42nd St, New York, NY
```

**Then geocodes and searches in NYC!**

---

## Examples

### Street Intersections

**Input:** `5th Ave and 42nd St`
**Becomes:** `5th Ave and 42nd St, New York, NY` ✅

**Input:** `Broadway & 34th`
**Becomes:** `Broadway & 34th, New York, NY` ✅

### Street Addresses

**Input:** `350 5th Ave`
**Becomes:** `350 5th Ave, New York, NY` ✅

**Input:** `123 Broadway`
**Becomes:** `123 Broadway, New York, NY` ✅

### Landmarks (Still Work)

**Input:** `Times Square`
**Becomes:** `Times Square, New York, NY` ✅

**Input:** `Grand Central`
**Becomes:** `Grand Central, New York, NY` ✅

### Already Has "New York" or "NY"

**Input:** `Times Square, New York`
**Stays:** `Times Square, New York` (not duplicated)

**Input:** `5th Ave, NY`
**Stays:** `5th Ave, NY` (not duplicated)

---

## Complete Search Examples

```
Search: noodles near 5th ave and 42nd st
         ↓
Location: "5th ave and 42nd st, New York, NY"
Query: "noodles"
```

```
Search: pizza near 350 5th ave
         ↓
Location: "350 5th ave, New York, NY"
Query: "pizza"
```

```
Search: sushi at broadway and 34th
         ↓
Location: "broadway and 34th, New York, NY"
Query: "sushi"
```

```
Search: tacos near times square
         ↓
Location: "times square, New York, NY"
Query: "tacos"
```

---

## Why This Helps

### Before (Generic)

**Input:** `5th Ave and 42nd St`
**Problem:** Could match 5th Ave in any city (Phoenix, Seattle, etc.)
**Result:** Wrong city ❌

### After (NYC-Only)

**Input:** `5th Ave and 42nd St`
**Auto-appends:** `, New York, NY`
**Result:** Always NYC ✅

---

## Benefits

1. ✅ **Type less** - No need to say "New York" every time
2. ✅ **No ambiguity** - Always gets NYC locations
3. ✅ **Works with numbered streets** - "5th Ave", "42nd St" = NYC
4. ✅ **Works with landmarks** - "Times Square" = NYC
5. ✅ **Smart** - Doesn't duplicate if you already said "NY"

---

## Usage

### Shortest Possible Input

```
Search: pizza near 5th and 42nd
```

That's it! System knows it's NYC.

### All Valid Formats

```
5th ave and 42nd st          ← Shortest
5th Ave & 42nd St           ← Also works
5th Avenue and 42nd Street  ← Also works
350 5th Ave                 ← Street number
times square                ← Landmark
grand central               ← Station
broadway and 34th           ← Intersection
```

**All automatically become NYC locations!**

---

## Override (If You Want Different City)

**Want different city?** Just include "NY" or "New York":

```
Search: pizza near 5th ave, albany, ny
         ↓
Location stays: "5th ave, albany, ny" (has "ny" so not changed)
```

But honestly, why would you? This is a **NYC restaurant agent!** 🗽

---

## Summary

**Before:**
```
Search: pizza near 5th Avenue and 42nd Street, New York, NY
```

**Now:**
```
Search: pizza near 5th and 42nd
```

**Much simpler!** ✨

---

**Try it:**
```bash
python matere_d_demo.py
```

**Type:**
```
Search: noodles near 5th and 42nd
```

**Gets:** NYC restaurants automatically! 🗽
