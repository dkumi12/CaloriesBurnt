import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Try to import the base64 encoded logo
try:
    from app.logo_base64 import LOGO_BASE64
    has_logo = True
except ImportError:
    has_logo = False

# Page configuration
st.set_page_config(
    page_title="MetriBurn - Smart Calorie Tracker",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Global styles */
    .stApp {
        background-color: #121212;
        font-family: 'Poppins', sans-serif;
    }
    
    .main .block-container {
        max-width: 800px;
        padding-top: 1rem;
    }
    
    /* Brand colors */
    :root {
        --brand-primary: #E57373;
        --brand-secondary: #4CAF50;
        --text-primary: #E0E0E0;
        --text-secondary: #9E9E9E;
        --bg-card: #1E1E1E;
        --bg-input: #2D2D2D;
    }
    
    /* Headers and text */
    h1, h2, h3, p, span, label {
        color: var(--text-primary) !important;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #E57373 0%, #FF8A80 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-primary) !important;
        font-size: 1.125rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    .tagline {
        text-align: center;
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 2rem !important;
    }
    
    /* Hide streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Section styling */
    h2 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Input styling */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background-color: var(--bg-input) !important;
        color: var(--text-primary) !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }
    
    /* Labels */
    .stSelectbox label,
    .stNumberInput label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%) !important;
        color: #121212 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.875rem !important;
        width: 100% !important;
        margin-top: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(229, 115, 115, 0.4) !important;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: rgba(25, 118, 210, 0.2) !important;
        border: 1px solid #1976D2 !important;
        color: var(--text-primary) !important;
    }
    
    /* Success box styling */
    div[data-baseweb="notification"] {
        background-color: rgba(76, 175, 80, 0.2) !important;
        border: 1px solid #4CAF50 !important;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: var(--bg-input);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #444;
        text-align: center;
    }
    
    [data-testid="metric-container"] > div:nth-child(1) {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    [data-testid="metric-container"] > div:nth-child(2) {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    [data-testid="metric-container"] > div:nth-child(3) {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--bg-input) !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }
    
    /* Divider styling */
    hr {
        border-color: #333 !important;
        margin: 2rem 0 !important;
    }
    
    /* Column gaps */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
    
    /* Footer branding */
    .footer-brand {
        text-align: center;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #333;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Load functions
@st.cache_data
def load_data():
    paths = ["data/engineered_exercise_dataset_expanded.csv", "data/engineered_exercise_dataset.csv"]
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Fix Unknown intensity
            if 'intensity' in df.columns and (df['intensity'] == 'Unknown').any():
                df.loc[df['intensity'] == 'Unknown', 'intensity'] = df.loc[df['intensity'] == 'Unknown', 'avg_calories'].apply(
                    lambda x: 'Low' if x < 250 else 'Moderate' if x < 450 else 'High'
                )
            return df
    st.error("Dataset not found!")
    return None

@st.cache_resource
def load_model():
    if os.path.exists("models/calories_prediction_model.pkl"):
        return joblib.load("models/calories_prediction_model.pkl")
    st.error("Model not found!")
    return None

def main():
    # Header with branding and logo
    if has_logo:
        # Direct implementation of header with inline HTML
        header_html = f"""
        <div style="margin: 1rem 0 2rem 0; text-align: center;">
            <!-- Logo with more zoom -->
            <div style="margin-bottom: 1rem;">
                <img src="data:image/png;base64,{LOGO_BASE64}" 
                     width="200" height="60" 
                     alt="MetriBurn Logo"
                     style="object-fit: contain;">
            </div>
            
            <!-- App description in bold with !important flags -->
            <div style="margin: 0 !important; padding: 0 !important; font-size: 1.4rem !important; font-weight: bold !important; color: #E0E0E0 !important; line-height: 1.4 !important; display: block !important;">
                Smart Calorie Tracking for Your Active Lifestyle
            </div>
            
            <!-- Powered by text in smaller font with !important flags -->
            <div style="margin: 0.2rem 0 0 0 !important; padding: 0 !important; font-size: 0.8rem !important; color: #9E9E9E !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; line-height: 1.2 !important; display: block !important;">
                Powered by Ever Booming Health and Wellness®
            </div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    else:
        # Fallback if no logo is available
        st.markdown("""
        <div style="margin: 1rem 0 2rem 0; text-align: center;">
            <div style="margin: 0; padding: 0; font-size: 1.4rem; font-weight: bold; color: #E0E0E0; line-height: 1.4;">
                Smart Calorie Tracking for Your Active Lifestyle
            </div>
            <div style="margin: 0.2rem 0 0 0; padding: 0; font-size: 0.8rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1.2;">
                Powered by Ever Booming Health and Wellness®
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Load resources
    df = load_data()
    model = load_model()
    if df is None or model is None:
        st.stop()
    
    # Activity Selection Section
    st.markdown("## Select Your Activity")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Activity selection
        activity_types = ["All"] + sorted(df['activity_type'].unique().tolist())
        selected_type = st.selectbox("Activity Category", activity_types)
        
        activities = df['activity'].tolist() if selected_type == "All" else df[df['activity_type'] == selected_type]['activity'].tolist()
        selected_activity = st.selectbox("Choose Activity 🏃", sorted(activities))
    
    with col2:
        # Activity info
        activity_data = df[df['activity'] == selected_activity].iloc[0]
        
        # Activity type emojis
        type_emojis = {
            'Cardio': '🏃',
            'Strength': '💪',
            'Sports': '⚽',
            'Flexibility': '🧘',
            'Other': '🏋️'
        }
        emoji = type_emojis.get(activity_data['activity_type'], '🎯')
        
        st.info(f"""
        {emoji} **Activity Type:** {activity_data['activity_type']}  
        🔥 **Intensity:** {activity_data['intensity']}  
        📊 **Avg Cal/Hour:** {activity_data['avg_calories']:.0f}
        """)
    
    st.markdown("---")
    
    # Your Details Section
    st.markdown("## Your Details")
    
    col3, col4 = st.columns(2)
    
    with col3:
        weight = st.number_input("Weight (lbs) ⚖️", 80, 400, 155, 5)
    
    with col4:
        duration = st.number_input("Duration (minutes) ⏱️", 5, 300, 30, 5)
    
    # Calculate button
    if st.button("CALCULATE MY BURN 🔥", type="primary", use_container_width=True):
        # Prepare prediction
        met = activity_data['estimated_met']
        calories_per_kg = activity_data['Calories per kg']
        
        # Create input data
        weight_ratios = {w: w/weight for w in [130, 155, 180, 205]}
        
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
            'normalized_calories_per_kg': [(calories_per_kg - df['Calories per kg'].min()) / 
                                          (df['Calories per kg'].max() - df['Calories per kg'].min())],
            'estimated_met': [met]
        })
        
        # Predict
        calories_per_hour = model.predict(input_data)[0]
        total_calories = calories_per_hour * duration / 60
        
        st.markdown("---")
        
        # Results Section
        st.success("## 🎯 Your Results")
        
        col5, col6, col7 = st.columns(3)
        
        with col5:
            st.metric("Total Burn 🔥", f"{total_calories:.0f}", "calories")
        with col6:
            st.metric("Per Hour 📈", f"{calories_per_hour:.0f}", "cal/hr")
        with col7:
            st.metric("Per Minute ⚡", f"{calories_per_hour/60:.1f}", "cal/min")
        
        # Food Equivalents
        st.markdown("### 🍔 Burn Equivalents")
        
        col8, col9, col10, col11 = st.columns(4)
        
        with col8:
            st.metric("🍕 Pizza", f"{total_calories/285:.1f}", "slices")
        with col9:
            st.metric("🍎 Apples", f"{total_calories/95:.1f}", "medium")
        with col10:
            st.metric("🍫 Chocolate", f"{total_calories/210:.1f}", "bars")
        with col11:
            st.metric("🥤 Soda", f"{total_calories/140:.1f}", "cans")
        
        # Motivational message
        if total_calories < 100:
            st.info("💚 **Good Start!** Every movement counts on your wellness journey.")
        elif total_calories < 300:
            st.info("👍 **Great Progress!** You're building healthy habits that last.")
        elif total_calories < 500:
            st.info("🔥 **Excellent Burn!** You're making serious progress toward your goals.")
        else:
            st.info("⚡ **Outstanding Performance!** You're a calorie-burning champion!")
        
        # Similar Activities
        with st.expander("🏋️ Discover Similar Activities"):
            similar = df[
                (df['avg_calories'] >= activity_data['avg_calories'] * 0.8) & 
                (df['avg_calories'] <= activity_data['avg_calories'] * 1.2) &
                (df['activity'] != selected_activity)
            ].head(5)
            
            if not similar.empty:
                st.write("**Activities with similar burn rates:**")
                for _, row in similar.iterrows():
                    intensity_emoji = {'Low': '🟢', 'Moderate': '🟡', 'High': '🔴'}.get(row['intensity'], '⚪')
                    
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"**{row['activity'][:40]}{'...' if len(row['activity']) > 40 else ''}**")
                        st.caption(f"{intensity_emoji} {row['intensity']} • {row['activity_type']}")
                    with col_b:
                        st.metric("Burn Rate", f"{row['avg_calories']:.0f}", "cal/hour", label_visibility="collapsed")
    
    # Footer
    st.markdown("""
    <div class="footer-brand">
        <p>MetriBurn™ © 2025 | Powered by Ever Booming Health and Wellness®</p>
        <p style="font-size: 0.75rem; margin-top: 0.5rem;">Empowering your fitness journey with data-driven insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()