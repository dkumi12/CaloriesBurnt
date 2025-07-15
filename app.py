import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import os
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Calories Burnt Prediction",
    page_icon="🔥",
    layout="wide"
)

# Define paths
MODEL_PATH = r"C:\Users\abami\OneDrive\Desktop\Projects\calories-burnt-prediction\models\calories_prediction_model.pkl"
DATA_PATH = r"C:\Users\abami\OneDrive\Desktop\Projects\calories-burnt-prediction\data\exercise_dataset.csv"
EXPANDED_DATA_PATH = r"C:\Users\abami\OneDrive\Desktop\Projects\calories-burnt-prediction\data\engineered_exercise_dataset_expanded.csv"

# Check if expanded dataset exists
import os
USE_EXPANDED = os.path.exists(EXPANDED_DATA_PATH)

# Create directories if they don't exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Function to load data
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        try:
            # Try expanded dataset first if it exists
            if USE_EXPANDED:
                df = pd.read_csv(EXPANDED_DATA_PATH)
                st.sidebar.info("Using expanded dataset (1,248 activities)")
                return df
            else:
                df = pd.read_csv(DATA_PATH)
                return df
        except FileNotFoundError:
            return None
# Function to preprocess data
def preprocess_data(df):
    if df is None:
        return None
    
    # Check if data is already preprocessed (has engineered features)
    required_engineered_features = ['avg_calories', 'intensity', 'activity_type', 'estimated_met']
    
    if all(col in df.columns for col in required_engineered_features):
        # Data is already engineered, just ensure numeric columns are correct type
        numeric_columns = ['130 lb', '155 lb', '180 lb', '205 lb', 'Calories per kg',
                          'avg_calories', 'calories_per_130lb', 'calories_per_155lb', 
                          'calories_per_180lb', 'calories_per_205lb', 'normalized_calories_per_kg', 
                          'estimated_met']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    # Otherwise, perform preprocessing
    # Clean column names
    df.columns = [col.strip().replace('\"', '') for col in df.columns]
    
    # Rename the first column if needed
    if 'Activity, Exercise or Sport (1 hour)' in df.columns:
        df = df.rename(columns={'Activity, Exercise or Sport (1 hour)': 'activity'})
    
    # Clean activity names
    if 'activity' in df.columns:
        df['activity'] = df['activity'].str.strip('\"')
    
    # Convert weight columns to numeric
    weight_columns = ['130 lb', '155 lb', '180 lb', '205 lb', 'Calories per kg']
    for col in weight_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Feature Engineering
    # Calculate average calories across different body weights
    df['avg_calories'] = df[['130 lb', '155 lb', '180 lb', '205 lb']].mean(axis=1)
    
    # Calories per specific body weights
    df['calories_per_130lb'] = df['130 lb']
    df['calories_per_155lb'] = df['155 lb']
    df['calories_per_180lb'] = df['180 lb']
    df['calories_per_205lb'] = df['205 lb']    
    # Intensity Categorization
    def categorize_intensity(activity, avg_calories=None):
        activity_lower = str(activity).lower()
        if any(x in activity_lower for x in ['light', 'mild', 'slow', 'leisure']):
            return 'Low'
        elif any(x in activity_lower for x in ['moderate', 'medium']):
            return 'Moderate'
        elif any(x in activity_lower for x in ['vigorous', 'fast', 'racing', 'high']):
            return 'High'
        else:
            # If we can't determine from activity name and have avg_calories, use that
            if avg_calories is not None:
                if avg_calories < 250:
                    return 'Low'
                elif avg_calories < 450:
                    return 'Moderate'
                else:
                    return 'High'
            return 'Moderate'  # Default to Moderate instead of Unknown
    
    # Apply with avg_calories if available
    if 'avg_calories' in df.columns:
        df['intensity'] = df.apply(lambda row: categorize_intensity(row['activity'], row.get('avg_calories', None)), axis=1)
    else:
        df['intensity'] = df['activity'].apply(lambda x: categorize_intensity(x))
    
    # Activity Type Categorization
    def categorize_activity_type(activity):
        activity_lower = str(activity).lower()
        if any(x in activity_lower for x in ['cycling', 'running', 'rowing', 'aerobics', 'dancing']):
            return 'Cardio'
        elif any(x in activity_lower for x in ['weight lifting', 'calisthenics', 'body building']):
            return 'Strength'
        elif any(x in activity_lower for x in ['yoga', 'stretching']):
            return 'Flexibility'
        else:
            return 'Other'
    
    df['activity_type'] = df['activity'].apply(categorize_activity_type)    
    # Additional derived features
    # Calories per kg normalized
    df['normalized_calories_per_kg'] = (df['Calories per kg'] - df['Calories per kg'].min()) / \
                                        (df['Calories per kg'].max() - df['Calories per kg'].min())
    
    # Metabolic Equivalent (MET) estimation
    df['estimated_met'] = df['avg_calories'] / 70  # Assuming base metabolic rate for a 70 kg person
    
    return df

# Function to train model
def train_model(df):
    if df is None:
        return None
    
    # Clean any remaining "Unknown" values in intensity
    if 'intensity' in df.columns and 'Unknown' in df['intensity'].values:
        # Replace Unknown with Moderate as default
        df.loc[df['intensity'] == 'Unknown', 'intensity'] = 'Moderate'
        st.warning("Found and fixed 'Unknown' intensity values in the dataset.")
    
    # Prepare features for selection
    X = df.select_dtypes(include=['float64', 'int64'])
    y = X['avg_calories']  # Target variable
    X = X.drop('avg_calories', axis=1)
    
    # Train a simple Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the model
    joblib.dump(model, MODEL_PATH)
    
    return model
# Function to load model
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        st.warning(f"Model not found at {MODEL_PATH}. Training a new model...")
        df = load_data()
        if df is not None:
            df = preprocess_data(df)
            model = train_model(df)
            return model
        return None

# Function to predict calories
def predict_calories(model, input_data):
    if model is None:
        return None
    
    prediction = model.predict(input_data)
    return prediction[0]

# Function to get feature importance
def get_feature_importance(model, feature_names):
    if model is None:
        return None
    
    importances = model.feature_importances_
    feature_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    return feature_imp
# Main function
def main():
    st.title("🔥 Calories Burnt Prediction")
    
    # Create sidebar
    st.sidebar.title("Navigation")
    
    # File uploader in sidebar
    uploaded_file = st.sidebar.file_uploader("Upload Exercise Dataset (CSV)", type=['csv'])
    
    page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Model Insights", "Prediction"])
    
    # Load data
    df = load_data(uploaded_file)
    if df is not None:
        df = preprocess_data(df)
        st.sidebar.success(f"Dataset loaded: {len(df)} activities")
    else:
        df = load_data()  # Try to load from default path
        if df is not None:
            df = preprocess_data(df)
    
    # Load or train model
    model = load_model()
    
    if page == "Home":
        st.header("Welcome to Calories Burnt Prediction App")
        st.markdown("""
        This application helps you predict the number of calories burned during different physical activities.
        
        ### Features:
        - **Data Exploration**: Explore the dataset and understand patterns
        - **Model Insights**: Learn what factors influence calorie burn
        - **Prediction**: Predict calories burned for your specific activity
        
        ### How it works:
        The prediction model is trained on a dataset containing various physical activities and their 
        corresponding calorie expenditure for different body weights. The model takes into account factors 
        like activity type, intensity, and other features to make accurate predictions.        
        ### Get Started:
        Use the sidebar to navigate through different sections of the app.
        """)
        
        if df is not None:
            st.subheader("Sample Data")
            st.dataframe(df.head())
        
    elif page == "Data Exploration":
        st.header("Data Exploration")
        
        if df is not None:
            # Data overview
            st.subheader("Dataset Overview")
            st.write(f"Total number of activities: {len(df)}")
            
            # Activity type distribution
            st.subheader("Activity Type Distribution")
            fig = px.pie(df, names='activity_type', title='Distribution of Activities by Type')
            st.plotly_chart(fig)
            
            # Intensity distribution
            st.subheader("Intensity Distribution")
            fig = px.pie(df, names='intensity', title='Distribution of Activities by Intensity')
            st.plotly_chart(fig)
            
            # Calories by activity type
            st.subheader("Calories by Activity Type")
            fig = px.box(df, x='activity_type', y='avg_calories', color='intensity',
                         title='Average Calories Burned by Activity Type and Intensity')
            st.plotly_chart(fig)            
            # Top calorie burning activities
            st.subheader("Top Calorie Burning Activities")
            top_activities = df.nlargest(10, 'avg_calories')[['activity', 'avg_calories']]
            fig = px.bar(top_activities, x='activity', y='avg_calories', 
                         title='Top 10 Activities for Burning Calories')
            st.plotly_chart(fig)
            
            # Weight comparison
            st.subheader("Calories Burned by Different Weights")
            weight_df = df.melt(id_vars=['activity'], 
                                value_vars=['130 lb', '155 lb', '180 lb', '205 lb'],
                                var_name='Weight', value_name='Calories')
            weight_sample = weight_df.sample(n=min(1000, len(weight_df)))
            fig = px.scatter(weight_sample, x='Weight', y='Calories', color='activity',
                             title='Calories Burned by Different Weights')
            st.plotly_chart(fig)
            
    elif page == "Model Insights":
        st.header("Model Insights")
        
        if model is not None:
            # Feature importance
            st.subheader("Feature Importance")
            feature_names = df.select_dtypes(include=['float64', 'int64']).drop('avg_calories', axis=1).columns
            feature_importance = get_feature_importance(model, feature_names)
            
            feature_df = pd.DataFrame(feature_importance, columns=['Feature', 'Importance'])
            fig = px.bar(feature_df, x='Feature', y='Importance', title='Feature Importance')
            st.plotly_chart(fig)            
            # Detailed feature importance table
            st.subheader("Detailed Feature Importance")
            st.dataframe(feature_df)
            
            # Explanation
            st.markdown("""
            ### What Influences Calorie Burn?
            
            The chart above shows the importance of different features in predicting calories burned.
            
            - **Higher values** indicate features that have a stronger influence on the prediction.
            - **Weight-related features** are typically very important, as body weight significantly affects calorie expenditure.
            - **Activity type and intensity** also play important roles in determining calories burned.
            
            The model considers all these factors together to make accurate predictions.
            """)
            
    elif page == "Prediction":
        st.header("Predict Calories Burned")
        
        if model is not None and df is not None:
            # Create input form
            st.subheader("Enter Activity Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Let user select from existing activities or choose custom
                activity_selection = st.radio("Choose an option:", ["Select from existing activities", "Custom activity"])
                
                if activity_selection == "Select from existing activities":
                    # Group activities by type for easier selection
                    activity_types = df['activity_type'].unique()
                    selected_type = st.selectbox("Activity Category", sorted(activity_types))
                    
                    # Filter activities by selected type
                    filtered_activities = df[df['activity_type'] == selected_type]['activity'].tolist()
                    selected_activity = st.selectbox("Select Activity", sorted(filtered_activities))
                    
                    # Get the data for selected activity
                    activity_data = df[df['activity'] == selected_activity].iloc[0]
                    activity_type = activity_data['activity_type']
                    intensity = activity_data['intensity']
                    
                    # Use the activity's values for prediction
                    calories_per_kg = activity_data['Calories per kg']
                    met = activity_data['estimated_met']
                    
                else:  # Custom activity
                    activity_type = st.selectbox("Activity Type", ["Cardio", "Strength", "Flexibility", "Sports", "Other"])
                    intensity = st.selectbox("Intensity Level", ["Low", "Moderate", "High"])
                    
                    st.info("💡 **Intensity Guide:**\n"
                           "- **Low**: Can talk normally, light effort\n"
                           "- **Moderate**: Can talk but breathing harder\n"
                           "- **High**: Difficult to talk, maximum effort")
                    
                    # Estimate MET based on activity type and intensity
                    met_values = {
                        ('Cardio', 'Low'): 4.0, ('Cardio', 'Moderate'): 7.0, ('Cardio', 'High'): 10.0,
                        ('Strength', 'Low'): 3.0, ('Strength', 'Moderate'): 5.0, ('Strength', 'High'): 8.0,
                        ('Flexibility', 'Low'): 2.0, ('Flexibility', 'Moderate'): 3.0, ('Flexibility', 'High'): 4.0,
                        ('Sports', 'Low'): 4.0, ('Sports', 'Moderate'): 6.0, ('Sports', 'High'): 9.0,
                        ('Other', 'Low'): 3.0, ('Other', 'Moderate'): 5.0, ('Other', 'High'): 7.0
                    }
                    met = met_values.get((activity_type, intensity), 5.0)
                    calories_per_kg = met * 1.05  # Approximate conversion
            
            with col2:
                weight = st.slider("Your Weight (lbs)", 100, 300, 155)
                duration = st.slider("Duration (minutes)", 10, 180, 60)
                
                st.write(f"**Activity Type:** {activity_type}")
                st.write(f"**Intensity:** {intensity}")
                
                if activity_selection == "Select from existing activities":
                    # Show average calories for this activity
                    st.write(f"**Average calories/hour for this activity:** {activity_data['avg_calories']:.0f}")
            
            
            # Calculate inputs for prediction
            weight_130_ratio = 130 / weight
            weight_155_ratio = 155 / weight
            weight_180_ratio = 180 / weight
            weight_205_ratio = 205 / weight
            
            calories_130 = met * 70 * weight_130_ratio
            calories_155 = met * 70 * weight_155_ratio
            calories_180 = met * 70 * weight_180_ratio
            calories_205 = met * 70 * weight_205_ratio
            
            # Create input data for prediction
            input_data = pd.DataFrame({
                '130 lb': [calories_130],
                '155 lb': [calories_155],
                '180 lb': [calories_180],
                '205 lb': [calories_205],
                'Calories per kg': [calories_per_kg],
                'calories_per_130lb': [calories_130],
                'calories_per_155lb': [calories_155],
                'calories_per_180lb': [calories_180],
                'calories_per_205lb': [calories_205],
                'normalized_calories_per_kg': [(calories_per_kg - df['Calories per kg'].min()) / 
                                              (df['Calories per kg'].max() - df['Calories per kg'].min())],
                'estimated_met': [met]
            })
            
            # Make prediction
            if st.button("Predict Calories", type="primary"):
                prediction = predict_calories(model, input_data)
                
                # Adjust for duration
                calories_for_duration = (prediction * duration / 60)
                
                st.success(f"### Estimated Calories Burned: **{calories_for_duration:.0f} calories**")
                
                # Provide context
                st.write(f"That's **{prediction:.0f} calories per hour**")
                
                # Provide some context
                if calories_for_duration < 100:
                    st.info("💡 This is a relatively low calorie burn. Great for recovery days!")
                elif calories_for_duration < 300:
                    st.info("💪 This is a moderate calorie burn. Good for general fitness!")
                elif calories_for_duration < 500:
                    st.info("🔥 This is a high calorie burn. Great for weight loss goals!")
                else:
                    st.info("⚡ This is a very high calorie burn. Excellent workout!")
                
                # Calorie equivalents
                st.subheader("Calorie Equivalents")
                col_eq1, col_eq2, col_eq3 = st.columns(3)
                
                with col_eq1:
                    st.metric("🍕 Pizza slices", f"{calories_for_duration/285:.1f}", 
                             help="Based on 285 calories per slice")
                with col_eq2:
                    st.metric("🍎 Apples", f"{calories_for_duration/95:.1f}", 
                             help="Based on 95 calories per medium apple")
                with col_eq3:
                    st.metric("🏃 Walking miles", f"{calories_for_duration/100:.1f}", 
                             help="Based on 100 calories per mile")                
                
                # Show similar activities
                st.subheader("Similar Activities Comparison")
                if activity_selection == "Select from existing activities":
                    # Show other activities with similar calorie burn
                    similar_calories = df[
                        (df['avg_calories'] >= activity_data['avg_calories'] * 0.8) & 
                        (df['avg_calories'] <= activity_data['avg_calories'] * 1.2) &
                        (df['activity'] != selected_activity)
                    ].head(5)
                    
                    if not similar_calories.empty:
                        st.write("Activities with similar calorie burn:")
                        similar_df = similar_calories[['activity', 'activity_type', 'intensity', 'avg_calories']].sort_values('avg_calories', ascending=False)
                        similar_df.columns = ['Activity', 'Type', 'Intensity', 'Avg Calories/Hour']
                        st.dataframe(similar_df, hide_index=True)
                else:
                    # Show activities matching the selected type and intensity
                    similar_activities = df[(df['activity_type'] == activity_type) & 
                                            (df['intensity'] == intensity)].head(5)
                    
                    if not similar_activities.empty:
                        st.write(f"Example {activity_type} activities at {intensity} intensity:")
                        similar_df = similar_activities[['activity', 'avg_calories']].sort_values('avg_calories', ascending=False)
                        similar_df.columns = ['Activity', 'Avg Calories/Hour']
                        st.dataframe(similar_df, hide_index=True)
                    else:
                        st.write("No similar activities found in our database.")
        else:
            st.error("Model not available. Please make sure the dataset is loaded correctly.")

if __name__ == "__main__":
    main()