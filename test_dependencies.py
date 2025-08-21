import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# Print versions to verify
print(f"pandas: {pd.__version__}")
print(f"numpy: {np.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
print(f"joblib: {joblib.__version__}")
print(f"plotly: {px.__version__}")

# Basic test of functionality
test_df = pd.DataFrame({'A': np.random.rand(10), 'B': np.random.rand(10)})
print("DataFrame created successfully")

# Test scikit-learn
rf = RandomForestRegressor(n_estimators=10)
print("RandomForestRegressor created successfully")

print("All imports and basic tests passed!")