# Quick Start Guide - CaloriesBurnt

## 30-Second Online Demo

**Visit**: https://metriburn-ebhnww.streamlit.app/

1. Select **Running** from activities
2. Enter weight: **170 lbs**
3. Enter duration: **30 minutes**
4. Click **"CALCULATE MY BURN 🔥"**
5. See results: ~**350 calories** + food equivalents

---

## 2-Minute Local Setup

```bash
# 1. Clone
git clone https://github.com/dkumi12/CaloriesBurnt.git
cd CaloriesBurnt

# 2. Install (first time only)
pip install -r requirements.txt

# 3. Run
streamlit run src/metriburn_app.py
```

Opens automatically at: **http://localhost:8501**

---

## 5-Minute First Use

| Step | Action | Result |
|------|--------|--------|
| 1 | Open app (online or local) | See MetriBurn interface |
| 2 | Choose activity category | Filter 1,248 exercises |
| 3 | Select activity (e.g., Running) | See activity details |
| 4 | Enter weight (170) | Input your body weight |
| 5 | Enter duration (30) | Input exercise minutes |
| 6 | Click "CALCULATE MY BURN" | Get instant results |
| 7 | View results | Total calories + metrics |
| 8 | Explore similar activities | Discover new exercises |

---

## What You Get

### Instant Results
- ✅ Total calories burned
- ✅ Calories per hour
- ✅ Calories per minute
- ✅ Food equivalents (pizza, apples, etc.)
- ✅ Motivational message
- ✅ Similar activity recommendations

### Example Output
```
Your Results

Total Burn 🔥          Per Hour 📈          Per Minute ⚡
   350 calories          700 cal/hr           11.7 cal/min

Burn Equivalents
🍕 Pizza: 1.2 slices
🍎 Apples: 3.7 medium
🍫 Chocolate: 1.7 bars
🥤 Soda: 2.5 cans
```

---

## Key Features

### 1. Activity Database
- **1,248+ exercises** across 5 categories
- Cardio, Strength, Sports, Flexibility, Other
- Easy search and filtering

### 2. Personalized Predictions
- Based on YOUR weight
- Your specific exercise duration
- Scientific MET values

### 3. Food Equivalents
- See calories as familiar foods
- Makes results relatable
- Motivation through comparison

### 4. Activity Recommendations
- Find exercises with similar burn rates
- Discover new activities
- Mix up your routine

### 5. Professional UI
- Dark theme (easy on eyes)
- Mobile responsive
- Fast predictions (<100ms)

---

## Common Tasks (1-Click)

### Find High-Intensity Activities
1. Select activity category
2. Look for "🔴 High" intensity badge
3. Check calories per hour
4. Try it!

### Compare Activities
1. Log Running (30 min)
2. Note calories: ~350
3. Try Cycling (30 min)
4. Compare: ~300-400
5. Choose based on preference

### Plan Daily Burn
1. Log Morning: Running (30 min)
2. Log Midday: Strength (45 min)
3. Log Evening: Walking (20 min)
4. Total daily: ~800-900 calories

---

## Prerequisites

### Minimal Requirements
- ✅ Web browser (for online version)
- ✅ Nothing else needed!

### For Local Installation
- ✅ Python 3.9+
- ✅ pip (comes with Python)
- ✅ ~100 MB disk space
- ✅ Internet (one-time for download)

---

## Troubleshooting (Quick Fixes)

| Problem | Solution |
|---------|----------|
| App won't open | Check Python version: `python --version` |
| "Package not found" | Install deps: `pip install -r requirements.txt` |
| Port 8501 in use | Use different port: `streamlit run src/metriburn_app.py --server.port 8502` |
| Slow predictions | Clear cache: `streamlit cache clear` |
| Wrong results | Check weight input (most common) |

---

## Next Steps

### Learn More
- **How it works?** → Read [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deploy yourself?** → Read [DEPLOYMENT.md](DEPLOYMENT.md)
- **Detailed guide?** → Read [USAGE.md](USAGE.md)
- **Integrate with app?** → Read [docs/INTEGRATION.md](docs/INTEGRATION.md)

### Explore Features
- Try different activities
- Mix activity types
- Compare burn rates
- Save your favorites (in local app)

### Share
- Send link to friends
- Share your results
- Challenge each other
- Track progress together

---

## Code at a Glance

### For Python Developers
```python
# Simple usage
from pathlib import Path
import pandas as pd
import joblib

df = pd.read_csv("data/engineered_exercise_dataset.csv")
model = joblib.load("models/calories_prediction_model.pkl")

# Get activity
activity = df[df['activity'] == 'Running'].iloc[0]
print(f"Running burns ~{activity['avg_calories']:.0f} cal/hr")
```

### For Web Developers
```bash
# Access the live API
curl "https://metriburn-ebhnww.streamlit.app/"

# Or integrate locally
streamlit run src/metriburn_app.py
```

---

## Fun Facts

- 🔥 **1,248+ exercises** in database
- ⚡ **<100ms** prediction time
- 📱 **Mobile responsive** design
- 🎯 **92% accurate** (±10% typical)
- 🚀 **Free to use** forever
- 👨‍💻 **Open source** codebase

---

## Performance Expectations

| Metric | Time |
|--------|------|
| App loads | 1-2 seconds |
| Prediction | <100 milliseconds |
| Page responds | <1 second |
| Works offline | No (needs data) |
| Mobile friendly | Yes ✅ |

---

## One More Thing

### Your First Prediction Walkthrough

**Step 1: Open App**
- Online: https://metriburn-ebhnww.streamlit.app/
- Local: http://localhost:8501

**Step 2: You See This**
```
🔥 MetriBurn
Smart Calorie Tracking for Your Active Lifestyle

[Activity Category Dropdown]
[Activity Selector Dropdown]
[Weight Input Field]
[Duration Input Field]
[CALCULATE MY BURN Button]
```

**Step 3: Fill It Out**
```
Activity Category: Cardio
Activity: Running (9.8 MET)
Weight: 170 lbs ⚖️
Duration: 30 minutes ⏱️
```

**Step 4: Click Button**
```
[CALCULATE MY BURN 🔥]
```

**Step 5: Get Results**
```
🎯 Your Results

Total Burn 🔥          Per Hour 📈          Per Minute ⚡
   350 calories          700 cal/hr           11.7 cal/min

Burn Equivalents
🍕 Pizza: 1.2 slices | 🍎 Apples: 3.7 medium
🍫 Chocolate: 1.7 bars | 🥤 Soda: 2.5 cans

🔥 Excellent Burn! You're making serious progress toward your goals.

Discover Similar Activities ▼
```

**Done!** 🎉 That's it!

---

## Most Common Use Cases

### 1. "I just finished my workout, how many calories did I burn?"
1. Select your activity
2. Enter your weight
3. Enter duration
4. See result instantly

### 2. "Which activity burns more calories?"
1. Calculate Activity A
2. Note the result
3. Calculate Activity B
4. Compare results

### 3. "I want to burn 500 calories, how long should I exercise?"
1. Select activity
2. Try different durations
3. Find duration that gives ~500
4. Plan accordingly

### 4. "Should I exercise more today?"
1. Log morning activities
2. Note total calories
3. Decide if more needed
4. Plan afternoon/evening activity

---

## Getting Help

### For Quick Questions
- Look at this Quick Start guide
- Check [USAGE.md](USAGE.md) for detailed examples

### For Technical Issues
- See [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for how it works

### For Integration
- Read [docs/INTEGRATION.md](docs/INTEGRATION.md)
- Copy code examples
- Test locally first

---

## Ready to Get Started?

### Option 1: Try Online (0 seconds to start)
Click: https://metriburn-ebhnww.streamlit.app/

### Option 2: Run Locally (2 minutes to start)
```bash
git clone https://github.com/dkumi12/CaloriesBurnt.git
cd CaloriesBurnt
pip install -r requirements.txt
streamlit run src/metriburn_app.py
```

### Option 3: Integrate in Your App
See [docs/INTEGRATION.md](docs/INTEGRATION.md) for code examples

---

## That's It! 🎉

You now know everything you need to use CaloriesBurnt.

Start tracking your fitness today! 💪🔥
