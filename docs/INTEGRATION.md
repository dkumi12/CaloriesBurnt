# CaloriesBurnt Integration Guide

## Overview

MetriBurnis designed to integrate seamlessly with health, fitness, and wellness applications. This guide shows how to embed calorie predictions into your own projects.

---

## Quick Integration (Python)

### Simplest Approach

```python
import pandas as pd
import joblib

# Load once at startup
df = pd.read_csv("data/engineered_exercise_dataset.csv")
model = joblib.load("models/calories_prediction_model.pkl")

def predict_calories(activity, weight_lbs, duration_minutes):
    """Predict calories burned for an activity"""
    
    # Find activity
    activity_data = df[df['activity'] == activity].iloc[0]
    
    # Extract features
    met = activity_data['estimated_met']
    calories_per_kg = activity_data['Calories per kg']
    
    # Calculate weight ratios
    weight_ratios = {w: w / weight_lbs for w in [130, 155, 180, 205]}
    
    # Build feature vector
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
    
    # Predict and scale
    calories_per_hour = float(model.predict(input_data)[0])
    total_calories = calories_per_hour * duration_minutes / 60
    
    return {
        'total_calories': round(total_calories, 2),
        'calories_per_hour': round(calories_per_hour, 2),
        'calories_per_minute': round(calories_per_hour / 60, 2),
        'intensity': activity_data['intensity'],
        'met': round(met, 1)
    }

# Use it
result = predict_calories('Running', 170, 30)
print(f"Burned {result['total_calories']} calories")
```

---

## Health App Integration (Django/Flask)

### Django Integration

```python
# your_app/models.py
from django.db import models

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    duration = models.IntegerField()  # minutes
    calories_burned = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Predict calories on save
        if not self.calories_burned:
            self.calories_burned = predict_calories(
                self.activity,
                self.user.weight_lbs,
                self.duration
            )
        super().save(*args, **kwargs)

# your_app/views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def log_workout(request):
    activity = request.data['activity']
    duration = request.data['duration']
    
    calories = predict_calories(activity, request.user.weight_lbs, duration)
    
    workout = Workout.objects.create(
        user=request.user,
        activity=activity,
        duration=duration,
        calories_burned=calories['total_calories']
    )
    
    return Response({'calories': calories})
```

### Flask Integration

```python
# app.py
from flask import Flask, request, jsonify
from models import CaloriePredictor

app = Flask(__name__)
predictor = CaloriePredictor()

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    result = predictor.predict(
        activity=data['activity'],
        weight_lbs=data['weight'],
        duration_minutes=data['duration']
    )
    return jsonify(result)

@app.route('/api/activities', methods=['GET'])
def get_activities():
    activities = predictor.get_all_activities()
    return jsonify(activities)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Mobile App Integration

### React Native

```javascript
// services/CalorieService.js
import axios from 'axios';

const API_URL = 'http://your-api.com/api';

export const CalorieService = {
  async predictCalories(activity, weight, duration) {
    try {
      const response = await axios.post(`${API_URL}/predict`, {
        activity,
        weight_lbs: weight,
        duration_minutes: duration
      });
      return response.data;
    } catch (error) {
      console.error('Prediction failed:', error);
      throw error;
    }
  },
  
  async getActivities() {
    const response = await axios.get(`${API_URL}/activities`);
    return response.data;
  }
};

// components/WorkoutTracker.js
import React, { useState, useEffect } from 'react';
import { CalorieService } from '../services/CalorieService';

export const WorkoutTracker = () => {
  const [activity, setActivity] = useState('');
  const [duration, setDuration] = useState(30);
  const [weight, setWeight] = useState(170);
  const [result, setResult] = useState(null);
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    CalorieService.getActivities().then(setActivities);
  }, []);

  const handleCalculate = async () => {
    const prediction = await CalorieService.predictCalories(
      activity,
      weight,
      duration
    );
    setResult(prediction);
  };

  return (
    <View>
      <Picker selectedValue={activity} onValueChange={setActivity}>
        {activities.map(a => (
          <Picker.Item key={a} label={a} value={a} />
        ))}
      </Picker>
      
      <TextInput
        placeholder="Weight (lbs)"
        value={String(weight)}
        onChangeText={w => setWeight(Number(w))}
      />
      
      <TextInput
        placeholder="Duration (minutes)"
        value={String(duration)}
        onChangeText={d => setDuration(Number(d))}
      />
      
      <Button title="Calculate" onPress={handleCalculate} />
      
      {result && (
        <Text>
          Burned {result.total_calories} calories
        </Text>
      )}
    </View>
  );
};
```

### iOS (SwiftUI)

```swift
import SwiftUI
import Combine

class CalorieCalculator: ObservableObject {
    @Published var result: CaloriePrediction?
    @Published var activities: [String] = []
    
    private let apiURL = "http://your-api.com/api"
    
    func predict(activity: String, weight: Double, duration: Double) {
        let url = URL(string: "\(apiURL)/predict")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "activity": activity,
            "weight_lbs": weight,
            "duration_minutes": duration
        ]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        URLSession.shared.dataTask(with: request) { data, _, _ in
            if let data = data,
               let prediction = try? JSONDecoder().decode(CaloriePrediction.self, from: data) {
                DispatchQueue.main.async {
                    self.result = prediction
                }
            }
        }.resume()
    }
    
    func fetchActivities() {
        let url = URL(string: "\(apiURL)/activities")!
        URLSession.shared.dataTask(with: url) { data, _, _ in
            if let data = data,
               let activities = try? JSONDecoder().decode([String].self, from: data) {
                DispatchQueue.main.async {
                    self.activities = activities
                }
            }
        }.resume()
    }
}

struct ContentView: View {
    @StateObject var calculator = CalorieCalculator()
    @State private var selectedActivity = ""
    @State private var weight = 170.0
    @State private var duration = 30.0
    
    var body: some View {
        VStack {
            Picker("Activity", selection: $selectedActivity) {
                ForEach(calculator.activities, id: \.self) { activity in
                    Text(activity).tag(activity)
                }
            }
            
            TextField("Weight (lbs)", value: $weight, format: .number)
            TextField("Duration (min)", value: $duration, format: .number)
            
            Button("Calculate") {
                calculator.predict(
                    activity: selectedActivity,
                    weight: weight,
                    duration: duration
                )
            }
            
            if let result = calculator.result {
                Text("Calories: \(result.total_calories)")
            }
        }
        .onAppear {
            calculator.fetchActivities()
        }
    }
}

struct CaloriePrediction: Codable {
    let total_calories: Double
    let calories_per_hour: Double
    let intensity: String
}
```

---

## REST API Integration

### API Endpoint Specification

**Base URL**: `https://your-api.com/api`

#### POST /predict

**Request**:
```json
{
  "activity": "Running",
  "weight_lbs": 170,
  "duration_minutes": 30
}
```

**Response**:
```json
{
  "activity": "Running",
  "weight_lbs": 170,
  "duration_minutes": 30,
  "total_calories": 350,
  "calories_per_hour": 700,
  "calories_per_minute": 11.67,
  "intensity": "High",
  "met": 9.8
}
```

#### GET /activities

**Response**:
```json
[
  "Running",
  "Walking",
  "Cycling",
  "Swimming",
  "Weightlifting",
  ...
]
```

#### GET /activities/search?q=running

**Response**:
```json
[
  {
    "activity": "Running",
    "type": "Cardio",
    "intensity": "High",
    "avg_calories": 680
  },
  {
    "activity": "Running (light jog)",
    "type": "Cardio",
    "intensity": "Moderate",
    "avg_calories": 500
  }
]
```

### cURL Examples

```bash
# Predict calories
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "activity": "Running",
    "weight_lbs": 170,
    "duration_minutes": 30
  }'

# Get all activities
curl http://localhost:8000/activities

# Search activities
curl "http://localhost:8000/activities/search?q=running"
```

---

## Wearable Device Integration

### Fitbit Integration

```python
import fitbit
from datetime import date

class FitbitCalorieIntegration:
    def __init__(self, client_id, client_secret):
        self.auth_client = fitbit.Fitbit(client_id, client_secret)
    
    def sync_workout(self, fitbit_activity_id, user_weight):
        # Get activity from Fitbit
        activity_data = self.auth_client.get_activity(fitbit_activity_id)
        
        # Map to MetriBurn activity
        activity_name = self.map_fitbit_activity(activity_data['activityName'])
        duration = activity_data['duration'] / 60000  # Convert ms to minutes
        
        # Get prediction
        prediction = predict_calories(activity_name, user_weight, duration)
        
        # Compare with Fitbit's calculation
        fitbit_burn = activity_data['caloriesSystemCalculated']
        
        return {
            'fitbit_calories': fitbit_burn,
            'predicted_calories': prediction['total_calories'],
            'difference': abs(fitbit_burn - prediction['total_calories'])
        }
    
    def map_fitbit_activity(self, fitbit_name):
        """Map Fitbit activity names to MetriBurn activities"""
        mapping = {
            'Running': 'Running',
            'Cycling': 'Cycling',
            'Walking': 'Walking',
            'Swimming': 'Swimming',
            'Weights': 'Weightlifting'
        }
        return mapping.get(fitbit_name, 'Other')
```

### Apple HealthKit Integration (iOS)

```swift
import HealthKit

class HealthKitIntegration {
    let healthStore = HKHealthStore()
    
    func logCaloriesToBurned(calories: Double) {
        let energyQuantity = HKQuantity(unit: .kilocalorie(), doubleValue: calories)
        let sample = HKQuantitySample(
            type: HKQuantityType.quantityType(
                forIdentifier: .activeEnergyBurned
            )!,
            quantity: energyQuantity,
            start: Date(),
            end: Date()
        )
        
        healthStore.save(sample) { success, error in
            if success {
                print("Logged to HealthKit")
            }
        }
    }
    
    func readWorkouts(completion: @escaping ([HKWorkout]) -> Void) {
        let predicate = HKQuery.predicateForWorkouts(
            withWorkoutActivityType: .other
        )
        
        let query = HKSampleQuery(
            sampleType: HKWorkoutType.workoutType(),
            predicate: predicate,
            limit: HKObjectQueryNoLimit,
            sortDescriptors: nil
        ) { _, results, _ in
            completion(results as? [HKWorkout] ?? [])
        }
        
        healthStore.execute(query)
    }
}
```

---

## Database Integration

### SQL Database

```python
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class WorkoutLog(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    activity = Column(String(100))
    duration = Column(Float)
    calories_burned = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

# Create tables
engine = create_engine('postgresql://user:pass@localhost/fitness')
Base.metadata.create_all(engine)

# Insert data
Session = sessionmaker(bind=engine)
session = Session()

workout = WorkoutLog(
    user_id=1,
    activity='Running',
    duration=30,
    calories_burned=350
)
session.add(workout)
session.commit()
```

### MongoDB Integration

```python
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['fitness_app']
workouts = db['workouts']

# Insert workout
workout_doc = {
    'user_id': '123',
    'activity': 'Running',
    'duration': 30,
    'calories_burned': 350,
    'created_at': datetime.now()
}

result = workouts.insert_one(workout_doc)

# Query workouts
user_workouts = workouts.find({'user_id': '123'})
total_calories = sum(w['calories_burned'] for w in user_workouts)
```

---

## Batch Processing

### Process Multiple Activities

```python
def process_workout_log(activities):
    """Calculate calories for multiple activities"""
    
    results = []
    total_calories = 0
    
    for activity, duration in activities:
        prediction = predict_calories(activity, 170, duration)
        results.append({
            'activity': activity,
            'duration': duration,
            'calories': prediction['total_calories']
        })
        total_calories += prediction['total_calories']
    
    return {
        'workouts': results,
        'daily_total': total_calories,
        'average_per_workout': total_calories / len(activities)
    }

# Usage
activities = [
    ('Running', 30),
    ('Strength Training', 45),
    ('Walking', 20)
]

summary = process_workout_log(activities)
print(f"Total Daily Burn: {summary['daily_total']} calories")
```

---

## Error Handling

```python
class CalorieCalculatorError(Exception):
    """Base exception for calorie calculator"""
    pass

class ActivityNotFoundError(CalorieCalculatorError):
    """Raised when activity doesn't exist"""
    pass

class InvalidInputError(CalorieCalculatorError):
    """Raised when input is invalid"""
    pass

def predict_calories_safe(activity, weight, duration):
    """Predict with error handling"""
    
    try:
        # Validate inputs
        if weight < 80 or weight > 400:
            raise InvalidInputError("Weight must be 80-400 lbs")
        
        if duration < 1 or duration > 480:
            raise InvalidInputError("Duration must be 1-480 minutes")
        
        # Check activity exists
        if activity not in df['activity'].values:
            raise ActivityNotFoundError(f"Activity '{activity}' not found")
        
        # Predict
        return predict_calories(activity, weight, duration)
        
    except ActivityNotFoundError as e:
        return {'error': str(e), 'suggestion': get_similar_activities(activity)}
    except InvalidInputError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': 'Prediction failed', 'details': str(e)}
```

---

## Caching for Performance

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedPredictor:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
    
    def predict_with_cache(self, activity, weight, duration):
        key = (activity, weight, duration)
        
        # Check cache
        if key in self.cache:
            result, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_duration:
                return result
        
        # Calculate if not cached
        result = predict_calories(activity, weight, duration)
        self.cache[key] = (result, datetime.now())
        
        return result
    
    def clear_old_cache(self):
        """Remove expired cache entries"""
        now = datetime.now()
        expired = [k for k, (_, ts) in self.cache.items() 
                   if now - ts > self.cache_duration]
        for key in expired:
            del self.cache[key]
```

---

## Summary

MetriBurn integrates into virtually any application through:
- **Direct Python usage** for simplicity
- **REST API** for remote access
- **Framework-specific** plugins (Django, Flask)
- **Mobile SDKs** (React Native, iOS, Android)
- **Wearable APIs** (Fitbit, Apple HealthKit)
- **Database storage** (SQL, MongoDB)

Choose the integration pattern that best fits your application architecture!
