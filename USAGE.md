# CaloriesBurnt Usage Guide

## Web Application

### For Fitness Enthusiasts

#### Step 1: Access the App
- **Online**: Visit https://metriburn-ebhnww.streamlit.app/
- **Local**: Run `streamlit run src/metriburn_app.py`

#### Step 2: Select Your Activity
1. Choose **Activity Category**
   - All (browse all 1,248 exercises)
   - Cardio (running, cycling, swimming)
   - Strength (weightlifting, resistance)
   - Sports (basketball, tennis, soccer)
   - Flexibility (yoga, pilates, stretching)
   - Other (walking, hiking, etc.)

2. Select **Specific Exercise**
   - Browse list of 1,248+ activities
   - View activity details (intensity, MET, avg burn)

#### Step 3: Enter Your Details
- **Weight**: Enter in pounds (80-400 lbs)
- **Duration**: Enter in minutes (5-300 minutes)

#### Step 4: Get Results
- Click **"CALCULATE MY BURN 🔥"** button
- View instant predictions:
  - Total calories burned
  - Calories per hour
  - Calories per minute

#### Step 5: Explore & Learn
- **Food Equivalents**: See calories as familiar foods
  - Pizza slices
  - Medium apples
  - Chocolate bars
  - Soda cans
- **Similar Activities**: Discover exercises with similar burn rates
- **Motivational Message**: Get encouraged based on your burn

---

## Usage Examples

### Example 1: Running Session
```
Activity: Running (Cardio)
Weight: 170 lbs
Duration: 30 minutes

Results:
├─ Total Calories: 350
├─ Per Hour: 700
├─ Per Minute: 11.7
└─ Food Equivalent: 1.2 pizzas
```

### Example 2: Strength Training
```
Activity: Weightlifting (Strength)
Weight: 185 lbs
Duration: 60 minutes

Results:
├─ Total Calories: 310
├─ Per Hour: 310
├─ Per Minute: 5.2
└─ Food Equivalent: 1.0 pizzas
```

### Example 3: HIIT Workout
```
Activity: HIIT Training (Cardio)
Weight: 160 lbs
Duration: 20 minutes

Results:
├─ Total Calories: 290
├─ Per Hour: 870
├─ Per Minute: 14.5
└─ Food Equivalent: 1.0 pizzas
```

### Example 4: Casual Walk
```
Activity: Walking (Other)
Weight: 155 lbs
Duration: 45 minutes

Results:
├─ Total Calories: 180
├─ Per Hour: 240
├─ Per Minute: 4.0
└─ Food Equivalent: 0.6 pizzas
```

---

## Tips for Accurate Results

### 1. Weight Accuracy
- Use your actual current weight
- If weight fluctuates, use average
- Accuracy improves with exact weight

### 2. Duration Includes Everything
- Total time spent on activity
- Includes warm-up periods
- Includes cool-down/rest periods
- For HIIT: includes rest intervals

### 3. Activity Selection
- Match activity description exactly
- Browse similar activities if unsure
- Check intensity level indicator
- View MET value (higher = more intense)

### 4. Interpreting Results
- Calories are estimates based on averages
- Individual metabolism varies ±20%
- Fitness level affects actual burn
- Technique/intensity affects results

---

## Understanding the Metrics

### Total Calories Burned
The estimated total calories you'll burn during the activity at your weight.

```
Calculation: (Calories per Hour) × (Duration in Minutes) ÷ 60
Example: 700 cal/hr × 30 min ÷ 60 = 350 calories
```

### Calories Per Hour
How many calories you'd burn if you did this activity for a full hour.

```
Used to compare activities
Example: Running = 700 cal/hr vs Walking = 240 cal/hr
```

### Calories Per Minute
Quick estimate of intensity - how much burn per minute.

```
Example: Running = 11.7 cal/min (high intensity)
Example: Walking = 4.0 cal/min (low intensity)
```

### MET (Metabolic Equivalent)
Scientific measure of exercise intensity:
- **< 1.5 MET**: Very light (sitting)
- **1.5-3 MET**: Light (walking)
- **3-6 MET**: Moderate (casual exercise)
- **> 6 MET**: Vigorous (intense exercise)

---

## Integration Examples

### For Developers

#### Python Integration
```python
import pandas as pd
import joblib

# Load resources
df = pd.read_csv("data/engineered_exercise_dataset.csv")
model = joblib.load("models/calories_prediction_model.pkl")

def calculate_calories(activity_name, weight_lbs, duration_minutes):
    # Find activity
    activity = df[df['activity'] == activity_name].iloc[0]
    
    # Extract features
    met = activity['estimated_met']
    calories_per_kg = activity['Calories per kg']
    
    # Calculate weight ratios
    weight_ratios = {w: w / weight_lbs for w in [130, 155, 180, 205]}
    
    # Prepare features
    input_data = pd.DataFrame({
        '130 lb': [met * 70 * weight_ratios[130]],
        '155 lb': [met * 70 * weight_ratios[155]],
        '180 lb': [met * 70 * weight_ratios[180]],
        '205 lb': [met * 70 * weight_ratios[205]],
        'Calories per kg': [calories_per_kg],
        'calories_per_130lb': [met * 70 * weight_ratios[130]],
        'calories_per_155lb': [met * 70 * weight_ratios[155]],
        'calories_per_180lb': [met * 70 * weight_ratios[180]],
        'calories_per_205lb': [met * 70 * weight_ratios[205]],
        'normalized_calories_per_kg': [
            (calories_per_kg - df['Calories per kg'].min()) /
            (df['Calories per kg'].max() - df['Calories per kg'].min())
        ],
        'estimated_met': [met],
    })
    
    # Predict
    calories_per_hour = float(model.predict(input_data)[0])
    total_calories = calories_per_hour * duration_minutes / 60
    
    return {
        'total_calories': round(total_calories, 2),
        'per_hour': round(calories_per_hour, 2),
        'per_minute': round(calories_per_hour / 60, 2),
        'intensity': activity['intensity'],
        'met': round(met, 1)
    }

# Usage
result = calculate_calories('Running', 170, 30)
print(f"Calories burned: {result['total_calories']}")
```

#### Batch Predictions
```python
activities = ['Running', 'Walking', 'Cycling', 'Swimming']
weight = 170
duration = 30

for activity in activities:
    result = calculate_calories(activity, weight, duration)
    print(f"{activity}: {result['total_calories']} calories")
```

#### Health App Integration
```python
class FitnessTracker:
    def __init__(self):
        self.df = pd.read_csv("data/engineered_exercise_dataset.csv")
        self.model = joblib.load("models/calories_prediction_model.pkl")
        self.user_weight = 170
    
    def log_activity(self, activity_name, duration_minutes):
        calories = self.calculate_calories(activity_name, self.user_weight, duration_minutes)
        self.save_to_database(activity_name, duration_minutes, calories)
        return calories
    
    def daily_total(self):
        # Sum all activities logged today
        pass
    
    def weekly_summary(self):
        # Average calories per day
        pass
    
    def activity_streak(self, activity_name):
        # Consecutive days doing activity
        pass
```

#### REST API Integration
```bash
# POST request to API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "activity": "Running",
    "weight_lbs": 170,
    "duration_minutes": 30
  }'

# Response
{
  "activity": "Running",
  "weight_lbs": 170,
  "duration_minutes": 30,
  "calories_per_hour": 700,
  "total_calories": 350,
  "intensity": "High",
  "met": 9.8
}
```

---

## Advanced Usage

### Finding Activities by Burn Rate
```python
# Find all activities burning ~300 cal/hour
target = 300
similar = df[
    (df['avg_calories'] >= target * 0.8) &
    (df['avg_calories'] <= target * 1.2)
]
print(similar[['activity', 'avg_calories', 'intensity']])
```

### Activity Comparison
```python
# Compare burn rates across activities
cardio = df[df['activity_type'] == 'Cardio'].sort_values('avg_calories', ascending=False)
strength = df[df['activity_type'] == 'Strength'].sort_values('avg_calories', ascending=False)

print("Top Cardio:", cardio.head(3))
print("Top Strength:", strength.head(3))
```

### High-Intensity Activities
```python
# Find high-intensity exercises
high_intensity = df[df['intensity'] == 'High'].sort_values('avg_calories', ascending=False)
print(high_intensity[['activity', 'avg_calories', 'estimated_met']].head(10))
```

### Track Daily Progress
```python
# Log multiple activities
activities = [
    ('Running', 30),
    ('Strength Training', 60),
    ('Walking', 20)
]

total_burn = 0
for activity, duration in activities:
    result = calculate_calories(activity, 170, duration)
    total_burn += result['total_calories']
    print(f"{activity}: {result['total_calories']:.0f} calories")

print(f"Total Daily Burn: {total_burn:.0f} calories")
```

---

## Frequently Asked Questions

### Q: How accurate are these predictions?
**A**: Predictions are validated against MET (Metabolic Equivalent) database standards. Actual individual burn varies ±20% based on:
- Personal metabolism
- Fitness level
- Technique/form
- Environmental conditions
- Recovery status

### Q: Why do similar activities have different burn rates?
**A**: Different techniques and intensity levels. For example:
- Casual jogging: 500 cal/hr
- Running (intense): 800 cal/hr
- Sprint: 1,000+ cal/hr

### Q: Can I use this for weight loss planning?
**A**: Yes, but consult healthcare professional. Use to:
- Estimate daily calorie burn
- Compare activities
- Track progress
- Set realistic goals

### Q: What if I can't find my specific activity?
**A**: Try variations:
- "Running" covers jogging, sprinting, trail running
- "Cycling" covers road, mountain, stationary
- "Sports" covers dozens of activities

### Q: How do I use this with my fitness tracker?
**A**: 
1. Log activity in your tracker
2. Get duration from tracker
3. Enter into MetriBurn
4. Compare with tracker data
5. Adjust for discrepancies

### Q: Can I use metric units?
**A**: Currently pounds only. To convert:
- Kilograms to pounds: kg × 2.205
- Example: 75 kg = 165 lbs

### Q: Does weather affect results?
**A**: Not directly calculated, but:
- Running uphill burns more
- Running downhill burns less
- Hot weather may increase slightly
- Cold weather may increase slightly

### Q: What about heart rate?
**A**: Not used in current model. MET values already account for typical heart rate responses. For precise data, use fitness tracker with HR sensor.

---

## Tips for Best Results

### Maximize Accuracy
1. ✓ Use your actual weight
2. ✓ Select precise activity
3. ✓ Be honest about duration
4. ✓ Consider difficulty level
5. ✓ Account for fitness level

### Explore Intelligently
1. ✓ Try similar activities
2. ✓ Mix activity types
3. ✓ Vary intensity levels
4. ✓ Track trends over time
5. ✓ Compare activities

### Health Goals
1. ✓ Set daily calorie targets
2. ✓ Mix cardio and strength
3. ✓ Gradually increase duration
4. ✓ Vary activities to prevent boredom
5. ✓ Track weight changes

---

## Support

- **Questions?** Check ARCHITECTURE.md for technical details
- **Deployment help?** See DEPLOYMENT.md
- **Data info?** Check docs/DATA.md
- **Integration?** See docs/INTEGRATION.md

---

## Key Takeaways

- **1,248+ activities** available to choose from
- **Accurate predictions** based on your weight
- **Food equivalents** show results in relatable terms
- **Activity recommendations** help discover new exercises
- **Professional interface** makes using a pleasure

Start exploring your fitness potential with MetriBurn today! 🔥
