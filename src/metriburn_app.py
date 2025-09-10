# src/metriburn_app.py
import os
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ------------------------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------------------------
st.set_page_config(
    page_title="MetriBurn - Smart Calorie Tracker",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------------------------
# Paths (robust across local + Streamlit Cloud)
# ------------------------------------------------------------------------------------
# This file lives at repo_root/src/metriburn_app.py → repo_root is parent of parent
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "static"

DATA_CANDIDATES = [
    DATA_DIR / "engineered_exercise_dataset_expanded.csv",
    DATA_DIR / "engineered_exercise_dataset.csv",
]
MODEL_PATH = MODELS_DIR / "calories_prediction_model.pkl"
LOGO_PATH = STATIC_DIR / "logo.png"

# ------------------------------------------------------------------------------------
# Custom CSS (branding)
# ------------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    .stApp { background-color: #121212; font-family: 'Poppins', sans-serif; }
    .main .block-container { max-width: 800px; padding-top: 1rem; }

    :root {
        --brand-primary: #E57373;
        --brand-secondary: #4CAF50;
        --text-primary: #E0E0E0;
        --text-secondary: #9E9E9E;
        --bg-card: #1E1E1E;
        --bg-input: #2D2D2D;
    }

    h1, h2, h3, p, span, label { color: var(--text-primary) !important; }

    .main-title {
        text-align: center; font-size: 3.5rem !important; font-weight: 800 !important;
        background: linear-gradient(135deg, #E57373 0%, #FF8A80 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important; letter-spacing: -1px;
    }

    .subtitle { text-align: center; color: var(--text-primary) !important; font-size: 1.125rem !important; margin-bottom: 0.25rem !important; }
    .tagline { text-align: center; color: var(--text-secondary) !important; font-size: 0.875rem !important; font-weight: 500 !important; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 2rem !important; }

    #MainMenu, footer, header { visibility: hidden; }

    h2 { color: var(--text-primary) !important; font-weight: 700 !important; margin-top: 1.5rem !important; margin-bottom: 1rem !important; }

    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background-color: var(--bg-input) !important; color: var(--text-primary) !important;
        border: 1px solid #444 !important; border-radius: 8px !important;
    }

    .stSelectbox label, .stNumberInput label {
        color: var(--text-primary) !important; font-weight: 500 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%) !important; color: #121212 !important;
        font-weight: 700 !important; border-radius: 8px !important; border: none !important;
        padding: 0.875rem !important; width: 100% !important; margin-top: 1rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.3s ease !important;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(229, 115, 115, 0.4) !important; }

    .stAlert { background-color: rgba(25,118,210,0.2) !important; border: 1px solid #1976D2 !important; color: var(--text-primary) !important; }

    div[data-baseweb="notification"] { background-color: rgba(76,175,80,0.2) !important; border: 1px solid #4CAF50 !important; }

    [data-testid="metric-container"] {
        background-color: var(--bg-input); border-radius: 12px; padding: 1.5rem; border: 1px solid #444; text-align: center;
    }
    [data-testid="metric-container"] > div:nth-child(1) { font-size: 0.875rem; color: var(--text-secondary); font-weight: 500; }
    [data-testid="metric-container"] > div:nth-child(2) { font-size: 2.5rem; font-weight: 700; color: #FFFFFF; }
    [data-testid="metric-container"] > div:nth-child(3) { font-size: 0.875rem; color: var(--text-secondary); }

    .streamlit-expanderHeader {
        background-color: var(--bg-input) !important; border: 1px solid #444 !important; border-radius: 8px !important;
        font-weight: 600 !important; color: var(--text-primary) !important;
    }

    hr { border-color: #333 !important; margin: 2rem 0 !important; }
    div[data-testid="stHorizontalBlock"] { gap: 1rem; }

    .footer-brand { text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #333; color: var(--text-secondary); font-size: 0.875rem; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# Loaders with caching
# ------------------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame | None:
    for path in DATA_CANDIDATES:
        if path.exists():
            df = pd.read_csv(path)
            # Fix "Unknown" intensity deterministically based on avg_calories
            if "intensity" in df.columns and (df["intensity"] == "Unknown").any():
                df.loc[df["intensity"] == "Unknown", "intensity"] = df.loc[
                    df["intensity"] == "Unknown", "avg_calories"
                ].apply(lambda x: "Low" if x < 250 else ("Moderate" if x < 450 else "High"))
            return df
    st.error("Dataset not found! Ensure your CSV exists at 'data/' in the repo root and the filename matches.")
    return None


@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    st.error("Model not found! Ensure your model exists at 'models/calories_prediction_model.pkl' in the repo root.")
    return None

# ------------------------------------------------------------------------------------
# Small style helper
# ------------------------------------------------------------------------------------
st.markdown("""
<style>
.single-line-heading {
    white-space: nowrap !important; overflow: visible !important;
    font-size: 1.3rem !important; font-weight: bold !important; margin: 0.5rem 0 !important;
    color: #E0E0E0 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------------
def main():
    # Header with centered logo + tagline
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=150)
        else:
            st.caption("Logo not found at static/logo.png")

        st.markdown(
            "<div style='text-align: center;'><p class='single-line-heading'>Smart Calorie Tracking for Your Active Lifestyle</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align: center; font-size: 0.8rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.5px;'>Powered by Ever Booming Health and Wellness®</div>",
            unsafe_allow_html=True,
        )

    # Load resources
    df = load_data()
    model = load_model()
    if df is None or model is None:
        st.stop()

    # -------------------- Activity Selection --------------------
    st.markdown("## Select Your Activity")
    left, right = st.columns([2, 1])

    with left:
        activity_types = ["All"] + sorted(df["activity_type"].dropna().unique().tolist())
        selected_type = st.selectbox("Activity Category", activity_types)

        if selected_type == "All":
            activities = df["activity"].dropna().tolist()
        else:
            activities = df.loc[df["activity_type"] == selected_type, "activity"].dropna().tolist()

        selected_activity = st.selectbox("Choose Activity 🏃", sorted(activities))

    with right:
        activity_data = df[df["activity"] == selected_activity].iloc[0]

        type_emojis = {
            "Cardio": "🏃",
            "Strength": "💪",
            "Sports": "⚽",
            "Flexibility": "🧘",
            "Other": "🏋️",
        }
        emoji = type_emojis.get(activity_data.get("activity_type", ""), "🎯")

        st.info(
            f"""
        {emoji} **Activity Type:** {activity_data['activity_type']}  
        🔥 **Intensity:** {activity_data['intensity']}  
        📊 **Avg Cal/Hour:** {activity_data['avg_calories']:.0f}
        """
        )

    st.markdown("---")

    # -------------------- Your Details --------------------
    st.markdown("## Your Details")
    c3, c4 = st.columns(2)
    with c3:
        weight = st.number_input("Weight (lbs) ⚖️", min_value=80, max_value=400, value=155, step=5)
    with c4:
        duration = st.number_input("Duration (minutes) ⏱️", min_value=5, max_value=300, value=30, step=5)

    # -------------------- Calculate --------------------
    if st.button("CALCULATE MY BURN 🔥", type="primary", use_container_width=True):
        met = activity_data["estimated_met"]
        calories_per_kg = activity_data["Calories per kg"]

        # Normalize per the original logic
        weight_ratios = {w: w / weight for w in [130, 155, 180, 205]}
        input_data = pd.DataFrame({
            "130 lb": [met * 70 * weight_ratios[130]],
            "155 lb": [met * 70 * weight_ratios[155]],
            "180 lb": [met * 70 * weight_ratios[180]],
            "205 lb": [met * 70 * weight_ratios[205]],
            "Calories per kg": [calories_per_kg],
            "calories_per_130lb": [met * 70 * weight_ratios[130]],
            "calories_per_155lb": [met * 70 * weight_ratios[155]],
            "calories_per_180lb": [met * 70 * weight_ratios[180]],
            "calories_per_205lb": [met * 70 * weight_ratios[205]],
            "normalized_calories_per_kg": [
                (calories_per_kg - df["Calories per kg"].min()) /
                (df["Calories per kg"].max() - df["Calories per kg"].min())
            ],
            "estimated_met": [met],
        })

        calories_per_hour = float(model.predict(input_data)[0])
        total_calories = calories_per_hour * duration / 60.0

        st.markdown("---")
        st.success("## 🎯 Your Results")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Burn 🔥", f"{total_calories:.0f}", "calories")
        with m2:
            st.metric("Per Hour 📈", f"{calories_per_hour:.0f}", "cal/hr")
        with m3:
            st.metric("Per Minute ⚡", f"{calories_per_hour/60:.1f}", "cal/min")

        # Food Equivalents
        st.markdown("### 🍔 Burn Equivalents")
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            st.metric("🍕 Pizza", f"{total_calories/285:.1f}", "slices")
        with e2:
            st.metric("🍎 Apples", f"{total_calories/95:.1f}", "medium")
        with e3:
            st.metric("🍫 Chocolate", f"{total_calories/210:.1f}", "bars")
        with e4:
            st.metric("🥤 Soda", f"{total_calories/140:.1f}", "cans")

        # Motivation
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
                (df["avg_calories"] >= activity_data["avg_calories"] * 0.8) &
                (df["avg_calories"] <= activity_data["avg_calories"] * 1.2) &
                (df["activity"] != selected_activity)
            ].head(5)

            if not similar.empty:
                st.write("**Activities with similar burn rates:**")
                for _, row in similar.iterrows():
                    intensity_emoji = {"Low": "🟢", "Moderate": "🟡", "High": "🔴"}.get(row["intensity"], "⚪")
                    a1, a2 = st.columns([3, 1])
                    with a1:
                        title = row["activity"]
                        st.write(f"**{title[:40]}{'...' if len(title) > 40 else ''}**")
                        st.caption(f"{intensity_emoji} {row['intensity']} • {row['activity_type']}")
                    with a2:
                        st.metric("Burn Rate", f"{row['avg_calories']:.0f}", "cal/hour", label_visibility="collapsed")

    # Footer
    st.markdown("""
    <div class="footer-brand">
        <p>MetriBurn™ © 2025 | Powered by Ever Booming Health and Wellness®</p>
        <p style="font-size: 0.75rem; margin-top: 0.5rem;">Empowering your fitness journey with data-driven insights</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
