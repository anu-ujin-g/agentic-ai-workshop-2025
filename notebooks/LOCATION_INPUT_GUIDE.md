# 📍 Location Input Guide

## Search Radius: 0.5 Miles

mATEre d' searches for restaurants within **0.5 miles (805 meters)** of your specified location.

**That's about:**
- 🚶 10-minute walk
- 🚕 2-minute drive
- 📏 8-10 city blocks in Manhattan

---

## Supported Location Formats

Google Geocoding API accepts many location formats. Here are the ones that work best:

### ✅ Street Addresses with Numbers

```
350 5th Avenue, New York
123 Broadway, NY
1000 6th Ave
42 W 48th St
```

**Best for:** Specific buildings, exact locations

---

### ✅ Street Intersections

```
5th Avenue and 42nd Street
Broadway & 34th St
5th Ave & E 23rd St
Lexington and 53rd
```

**Best for:** General areas, neighborhoods
**Note:** Use "and" or "&" between streets

---

### ✅ Landmarks

```
Empire State Building
Grand Central Terminal
Times Square
Central Park
Rockefeller Center
Madison Square Garden
Brooklyn Bridge
```

**Best for:** Famous locations, easy to remember

---

### ✅ Transit Stations

```
Grand Central Station
Penn Station
Union Square Station
Times Square-42nd Street Station
Columbus Circle Station
```

**Best for:** Near subway/train stations

---

### ✅ Neighborhoods

```
SoHo, New York
Greenwich Village, NYC
Upper West Side, Manhattan
Williamsburg, Brooklyn
```

**Best for:** Exploring a general area

---

### ✅ Coordinates (lat,lng)

```
40.758896,-73.985130
40.7580,-73.9855
```

**Best for:** Exact GPS locations

---

## What Works Best

### Recommended Format Priority:

1. **Full street address with number** → Most accurate
   - `350 5th Avenue, New York, NY`

2. **Intersection** → Good for general area
   - `5th Ave & 42nd St`

3. **Landmark/Station** → Easy and reliable
   - `Grand Central Terminal`

4. **Neighborhood** → Broader area
   - `SoHo, New York`

---

## Examples by Use Case

### "I'm at a specific building"
```
📍 Your location: 350 5th Avenue, New York
📍 Your location: 30 Rockefeller Plaza
📍 Your location: 1 World Trade Center
```

### "I'm at an intersection"
```
📍 Your location: 5th Ave and 42nd St
📍 Your location: Broadway & 34th St
📍 Your location: Lexington and 59th
```

### "I'm near a landmark"
```
📍 Your location: Empire State Building
📍 Your location: Central Park
📍 Your location: Brooklyn Bridge
```

### "I'm at a subway station"
```
📍 Your location: Grand Central Station
📍 Your location: Penn Station
📍 Your location: Union Square Station
```

### "I want to explore a neighborhood"
```
📍 Your location: SoHo, New York
📍 Your location: Williamsburg, Brooklyn
📍 Your location: Upper East Side
```

---

## How It Works Behind the Scenes

1. **You enter:** `"5th Ave and 42nd St"`

2. **Google Geocoding converts to coordinates:**
   ```
   Latitude: 40.753596
   Longitude: -73.976522
   ```

3. **Google Places searches within 0.5 miles:**
   ```
   Find all restaurants within 805 meters of (40.753596, -73.976522)
   ```

4. **Results are stored and displayed:**
   ```
   Found 45 restaurants within 0.5 miles
   ```

---

## Tips for Best Results

### ✅ DO:
- Include city/state for smaller locations: `"Main St, Albany, NY"`
- Use well-known landmarks: `"Grand Central"`
- Use complete station names: `"Penn Station"` not just `"Penn"`
- Be specific with street numbers when possible: `"350 5th Ave"`

### ❌ DON'T:
- Use ambiguous names: `"The park"` (which park?)
- Forget the city for common street names: `"Main Street"` (which city?)
- Use abbreviations Google might not recognize
- Use slang or informal names: `"GCT"` instead of `"Grand Central"`

---

## Troubleshooting Location Input

### "Could not find location"

**Common causes:**
1. Typo in address/landmark name
2. Missing city/state for common street names
3. Using informal abbreviations

**Solutions:**
- Add city: `"5th Ave, New York"` instead of just `"5th Ave"`
- Use full names: `"Grand Central Terminal"` not `"GCT"`
- Try a nearby landmark instead
- Use coordinates as last resort

### "No restaurants found"

**Common causes:**
1. Location is in a non-commercial area (residential, parks)
2. Very new developments with no restaurant data yet
3. Area outside of major cities

**Solutions:**
- Try a nearby commercial intersection
- Use a major landmark in the area
- Expand to a neighborhood search

---

## Real-World Examples

### Scenario 1: Tourist at Times Square
```
📍 Your location: Times Square
✅ Finds restaurants in Theater District, Hell's Kitchen area
```

### Scenario 2: Office worker in Midtown
```
📍 Your location: 350 5th Avenue
✅ Finds restaurants around Empire State Building area
```

### Scenario 3: Commuter at Grand Central
```
📍 Your location: Grand Central Terminal
✅ Finds restaurants in Midtown East
```

### Scenario 4: Meeting at an intersection
```
📍 Your location: 5th Ave and 42nd St
✅ Finds restaurants in Bryant Park area
```

### Scenario 5: Exploring Brooklyn
```
📍 Your location: Williamsburg, Brooklyn
✅ Finds restaurants in Williamsburg neighborhood
```

---

## Quick Reference

| Input Type | Example | Use When |
|------------|---------|----------|
| Full Address | `350 5th Ave, New York` | You know exact address |
| Intersection | `5th Ave & 42nd St` | You know cross streets |
| Landmark | `Grand Central Terminal` | Near famous place |
| Station | `Penn Station` | At subway/train station |
| Neighborhood | `SoHo, New York` | Exploring an area |
| Coordinates | `40.758,-73.985` | Using GPS/maps |

---

## Summary

**Search Radius:** 0.5 miles (10-minute walk)

**Best Input Formats:**
1. Street address with number
2. Intersection (use & or "and")
3. Landmark/station
4. Neighborhood

**Always include:** City/state for less common locations

**Google handles:** Address normalization, typos, variations

---

**Now you know how to enter any location! 📍**
