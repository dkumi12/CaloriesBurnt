# MetriBurn - Calorie Prediction App

Machine learning-powered web application for predicting calories burned during physical activities.

**Powered by Ever Booming Health and Wellness®**

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dkumi12/CaloriesBurnt/main/metriburn_app.py)

## ✨ Features

- 1,248+ physical activities
- Personalized predictions based on weight & duration
- Food equivalent visualizations
- Activity recommendations
- Modern dark theme UI

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **ML Model**: Random Forest (Scikit-learn)
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/dkumi12/CaloriesBurnt.git
cd CaloriesBurnt

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run metriburn_app.py
```

## 📊 Project Structure

```
├── metriburn_app.py    # Main application
├── app.py              # Analysis dashboard (4 tabs)
├── requirements.txt    # Dependencies
├── data/              # Datasets
├── models/            # Trained ML model
└── .streamlit/        # Theme configuration
```

## 🎯 Usage

1. Select an activity category
2. Choose specific activity
3. Enter your weight and duration
4. Get personalized calorie prediction

## 📝 License

© 2025 Ever Booming Health and Wellness®. All rights reserved.