# Deployment Guide for MetriBurn App

## 1. Requirements.txt Update

The original requirements.txt file specified packages that are incompatible with Python 3.13 (used by Streamlit Cloud). The main issue was:

- `numpy==1.24.3` depends on the `distutils` module, which was removed in Python 3.13
- `pandas==1.5.3` is not compatible with the newer Python version

Your requirements.txt has been updated with compatible versions:

```
streamlit==1.32.0
pandas==2.1.4
numpy==1.26.4
matplotlib==3.8.3
seaborn==0.13.2
scikit-learn==1.4.1
joblib==1.3.2
plotly==5.19.0
```

## 2. Push Changes to GitHub

1. Open a terminal/command prompt
2. Navigate to your project directory:
   ```
   cd C:\Users\abami\OneDrive\Desktop\Projects\calories-burnt-prediction
   ```
3. Add the updated requirements.txt file:
   ```
   git add requirements.txt
   ```
4. Commit the changes:
   ```
   git commit -m "Update dependencies for Python 3.13 compatibility"
   ```
5. Push to GitHub:
   ```
   git push origin main
   ```

## 3. Redeploy on Streamlit Cloud

1. After pushing your changes, go to [Streamlit Cloud](https://streamlit.io/cloud)
2. If needed, select your repository and branch (main)
3. Streamlit Cloud should automatically detect the changes and rebuild your app
4. Monitor the build logs for any additional issues

## 4. Potential Issues & Solutions

If you encounter any other errors during deployment:

1. **ImportError for specific functions**: Some functions may have been renamed or moved in newer library versions. You might need to update your code accordingly.

2. **Incompatible model files**: If your trained model was created with an older scikit-learn version, you might need to retrain it with the updated library.

3. **Streamlit widget changes**: Some Streamlit widgets may have changed behavior between versions. Test all interactive elements after deployment.

## 5. Local Testing

Before deploying, you can test locally with the new dependencies:

1. Create a new virtual environment:
   ```
   python -m venv venv_new
   venv_new\Scripts\activate
   ```

2. Install the updated requirements:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run metriburn_app.py
   ```

4. Test all functionality to ensure compatibility with the updated packages.

## Questions or Issues?

If you encounter any issues with the deployment, feel free to contact Claude for further assistance!