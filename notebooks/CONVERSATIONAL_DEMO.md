# 🗣️ Conversational Demo Guide

## New Features

### 1. Natural Language Prompts
- **"What are you craving?"** - Ask naturally (e.g., "korean bbq near times square")
- **"Where are you?"** - Only if location wasn't mentioned
- **"Are these good, or want to see more?"** - Request different results
- **"Want to give feedback?"** - Optional feedback in natural language

### 2. Show More Results
You can now request to see different restaurants if the first set doesn't look good!

---

## Example Sessions

### Session 1: Finding Korean BBQ

```
Welcome to mATEre d'!

What are you craving? korean bbq near times square

1. Jongro BBQ Market | AYCE Korean BBQ Midtown
   Korean • $$ • ⭐ 4.8/5 (1026 reviews)
   Match: 67.2%
   18 W 38th St, New York

2. KPOT Korean BBQ & Hot Pot
   Korean • $$ • ⭐ 4.9/5 (2449 reviews)
   Match: 56.1%
   310 W 38th St, New York

Are these good, or want to see more? show me more

1. Don Don Korean BBQ
   Korean • $$ • ⭐ 4.5/5 (286 reviews)
   Match: 55.9%
   37 W 43rd St, New York

2. K-Bap & Wings | Korean
   Korean • $$ • ⭐ 4.7/5 (1404 reviews)
   Match: 37.4%
   62 W 56th St, New York

Are these good, or want to see more? these look great

Want to give feedback? The first one is perfect!
✅ Thanks!
```

---

### Session 2: Quick Pizza Search

```
Welcome to mATEre d'!

What are you craving? cheap pizza near grand central

1. $1.50 Fresh Pizza
   Italian • $ • ⭐ 4.5/5 (2569 reviews)
   Match: 87.8%
   143 W 40th St, New York

2. $1.50 Fresh Pizza
   Italian • $ • ⭐ 4.5/5 (2415 reviews)
   Match: 86.4%
   151 E 43rd St, New York

Are these good, or want to see more? perfect

Want to give feedback? no thanks
```

---

## How It Works

### "Are these good, or want to see more?"

**Triggers for showing more:**
- "more"
- "different"
- "other"
- "else"
- "another"
- "next"

**Examples:**
- "show me more"
- "want different options"
- "let me see other places"
- "got anything else?"

**Accepts results:**
- "these are good"
- "perfect"
- "yes"
- "looks great"
- Basically anything that doesn't contain the trigger words above

---

## Feedback

### Natural Language Feedback

**Specify which restaurant:**
- "The **first** one looks great!"
- "**Second** place was awesome"
- "**1** is perfect"
- "**2** looks good"

**Express sentiment:**
- Positive: "love", "great", "awesome", "perfect", "amazing"
- Negative: "bad", "hate", "terrible", "awful"

**Give vibe score:**
- Just mention a number 1-5 anywhere in your feedback
- "The first one is a 5!"
- "Second place, maybe a 3"

**Examples:**
- "The first one looks amazing! 5 stars"
  → Restaurant #1, liked=True, vibe_score=5

- "Second place was okay, 3 out of 5"
  → Restaurant #2, liked=True, vibe_score=3

- "The first one was terrible"
  → Restaurant #1, liked=False

- "no thanks"
  → No feedback saved

---

## Tips

1. **Search naturally**: "I want noodles near times square"
2. **Request more**: Say "more", "different", or "next" to see more restaurants
3. **Skip feedback**: Just say "no" or "no thanks"
4. **Be specific**: Mention "first" or "second" when giving feedback
5. **Explore options**: You can request more results multiple times until you find what you like

---

## Full Conversation Flow

```
1. "What are you craving?"
   → Enter your search query

2. [If no location] "Where are you?"
   → Enter location

3. [Shows 2 restaurants]

4. "Are these good, or want to see more?"
   → Say "more" to see different results
   → Or say "good" to continue

5. [Repeat step 3-4 if you want more]

6. "Want to give feedback?"
   → Optional: Give natural language feedback
   → Or say "no thanks" to skip
```

---

## Run It

```bash
python matere_d_demo.py
```

That's it! Enjoy your conversational restaurant search! 🍽️
