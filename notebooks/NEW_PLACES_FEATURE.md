# 🆕 New Places Feature

## Overview

The agent now understands when you want to try NEW restaurants and automatically excludes places you've already visited!

---

## How It Works

### 1. Mark a Restaurant as Visited

When giving feedback, mention that you visited:

```
Want to give feedback? visited the first one, it was great!
Want to give feedback? I went to the second place, 5 stars
Want to give feedback? tried it, loved it
Want to give feedback? been there, amazing food
```

**Trigger words:**
- "visited"
- "went"
- "been there"
- "tried it"

---

### 2. Search for New Places

Use keywords to indicate you want NEW restaurants:

```
What are you craving? new korean bbq near times square
What are you craving? I want to try a different italian place
What are you craving? looking for another pizza spot
What are you craving? never been to this area, want sushi
```

**Trigger words:**
- "new"
- "different"
- "another"
- "try something"
- "never been"

---

## Example Flow

### Step 1: Visit a Restaurant

```
What are you craving? korean bbq near times square

1. Jongro BBQ Market | AYCE Korean BBQ Midtown
   Korean • $$ • ⭐ 4.8/5 (1026 reviews)

2. KPOT Korean BBQ & Hot Pot
   Korean • $$ • ⭐ 4.9/5 (2449 reviews)

Are these good, or want to see more? good

Want to give feedback? visited the first one, it was amazing!
✅ Thanks!
```

### Step 2: Search for NEW Korean BBQ

```
What are you craving? I want to try a new korean bbq near times square

1. KPOT Korean BBQ & Hot Pot  ← NEW (not visited yet)
   Korean • $$ • ⭐ 4.9/5 (2449 reviews)

2. Don Don Korean BBQ  ← NEW (not visited yet)
   Korean • $$ • ⭐ 4.5/5 (286 reviews)
```

Notice: **Jongro BBQ Market** is excluded because you visited it!

---

## Additional Examples

### Example 1: Try Different Pizza

```
# First search
What are you craving? cheap pizza near grand central

1. $1.50 Fresh Pizza
2. Joe's Pizza

Want to give feedback? went to the first one
✅ Thanks!

# Next search
What are you craving? want to try different cheap pizza near grand central

1. Joe's Pizza  ← NEW
2. Prince Street Pizza  ← NEW

# $1.50 Fresh Pizza is excluded!
```

---

### Example 2: Another Sushi Place

```
# First visit
What are you craving? sushi near times square
...
Want to give feedback? visited it, great omakase
✅ Thanks!

# Second search
What are you craving? looking for another sushi place near times square

# Shows different sushi restaurants, excluding the visited one
```

---

## How the Agent Knows

### Visited Tracking

The agent tracks visited restaurants in the SQLite database:

```sql
SELECT DISTINCT rh.restaurant_name
FROM user_feedback uf
JOIN recommendation_history rh ON uf.recommendation_id = rh.recommendation_id
WHERE uf.visited = 1
```

### Filtering Logic

When you use "new" keywords:
1. Agent queries database for visited restaurant names
2. Filters them out from search results
3. Shows only unvisited restaurants

---

## Benefits

✅ **No Repeats**: Never get recommended places you've already been to
✅ **Exploration**: Discover new restaurants while staying in your preferred cuisine
✅ **Smart Learning**: Agent remembers your history across sessions
✅ **Natural Language**: Just say "new" or "different" - no complex syntax

---

## Keyword Reference

### To Mark as Visited (in feedback)
- visited
- went
- been there
- tried it

### To Request New Places (in query)
- new
- different
- another
- try something
- never been

---

## Combined with Other Filters

You can combine "new" with other filters:

```
new cheap pizza near times square
→ Cheap ($), Italian, NOT visited

I want to try a different expensive italian place
→ Italian, $$$, NOT visited

looking for another korean bbq
→ Korean, NOT visited
```

---

## Notes

- If you mark multiple restaurants as visited, ALL will be excluded
- If all restaurants have been visited, agent shows all (fallback)
- Works across sessions (persistent in database)
- Only excludes if `visited=True` in feedback

---

## Testing It Out

```bash
# Visit a place
echo "korean bbq near times square
good
visited the first one, loved it" | python matere_d_demo.py

# Search for new ones
echo "new korean bbq near times square
good
no" | python matere_d_demo.py
```

You'll see different results! 🎉
