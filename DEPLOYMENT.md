# CaloriesBurnt Deployment Guide

## Current Deployment (Streamlit Cloud)

### Prerequisites
- GitHub repository
- Streamlit Cloud account (free)
- Python 3.11+

### How It Works
MetriBurn is currently deployed on Streamlit Cloud with automatic deployment on every GitHub push.

**Live URL**: https://metriburn-ebhnww.streamlit.app/

### Setup Steps for Your Own Deployment

1. **Sign Up for Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub account
   - Grant necessary permissions

2. **Deploy the App**
   - Click "New app"
   - Select your GitHub repository
   - Set main file: `src/metriburn_app.py`
   - Click "Deploy"

3. **Auto-Updates**
   - Every push to main automatically triggers deployment
   - Deployment takes 2-3 minutes
   - Previous versions archived automatically

### Required Files
All required files are already in the repository:
- `requirements.txt` ✓ (Python dependencies)
- `runtime.txt` ✓ (Python version specification)
- `packages.txt` ✓ (System packages)
- `src/metriburn_app.py` ✓ (Main application)
- `models/calories_prediction_model.pkl` ✓ (Trained ML model)
- `data/engineered_exercise_dataset.csv` ✓ (Exercise database)

---

## Local Development

### Prerequisites
- Python 3.11+
- pip or conda
- Git

### Installation Steps

**1. Clone the Repository**
```bash
git clone https://github.com/dkumi12/CaloriesBurnt.git
cd CaloriesBurnt
```

**2. Create Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run Locally**
```bash
streamlit run src/metriburn_app.py
```

App will open at: http://localhost:8501

### Development with Hot Reload
```bash
streamlit run src/metriburn_app.py \
  --logger.level=debug \
  --server.runOnSave=true
```

---

## Troubleshooting

### Issue: "Dataset not found"
**Error**: The app shows error message about missing dataset

**Solution**: Ensure CSV file exists:
```bash
ls data/
# Should show: engineered_exercise_dataset.csv or engineered_exercise_dataset_expanded.csv
```

**Fix**: Download the file or check file path in `src/metriburn_app.py`

### Issue: "Model not found"
**Error**: The app shows error about missing model file

**Solution**: Ensure model file exists:
```bash
ls models/
# Should show: calories_prediction_model.pkl
```

**Fix**: Train the model or restore from backup

### Issue: Slow App Startup
**Problem**: Takes >5 seconds to load

**Solution**: Check Streamlit caching:
- Verify `@st.cache_data` decorator is present
- Clear cache: `streamlit cache clear`
- Restart: `streamlit run src/metriburn_app.py`

### Issue: Dependencies Not Installed
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
# Or install specific packages:
pip install streamlit==1.30.0 scikit-learn pandas numpy
```

### Issue: Port Already in Use
**Error**: `Address already in use` for port 8501

**Solution**:
```bash
# Use different port
streamlit run src/metriburn_app.py --server.port 8502

# Or kill process using port 8501
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501   # Windows
```

---

## Alternative Deployments

### Option 1: Docker Container

**Create Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/metriburn_app.py"]
```

**Build and Run**:
```bash
docker build -t metriburn .
docker run -p 8501:8501 metriburn
```

**Deploy to Docker Hub**:
```bash
docker login
docker tag metriburn yourusername/metriburn:latest
docker push yourusername/metriburn:latest
```

---

### Option 2: Heroku Deployment

**1. Create Procfile**:
```
web: sh setup.sh && streamlit run src/metriburn_app.py
```

**2. Create setup.sh**:
```bash
mkdir -p ~/.streamlit
echo "[theme]
primaryColor = \"#E57373\"
backgroundColor = \"#121212\"
secondaryBackgroundColor = \"#1E1E1E\"
textColor = \"#E0E0E0\"
" > ~/.streamlit/config.toml
```

**3. Deploy**:
```bash
heroku login
heroku create metriburn-app
git push heroku main
```

---

### Option 3: AWS EC2

**1. Launch EC2 Instance** (t2.micro eligible for free tier)

**2. SSH into Instance**:
```bash
ssh -i key.pem ubuntu@ec2-instance-ip
```

**3. Install Dependencies**:
```bash
sudo apt update
sudo apt install python3.11 python3-pip
pip install -r requirements.txt
```

**4. Run App**:
```bash
nohup streamlit run src/metriburn_app.py --server.port 80 &
```

**5. Access**: http://your-ec2-public-ip

---

### Option 4: REST API (FastAPI)

For integration with other applications, create FastAPI server:

**Create `api/main.py`**:
```python
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load resources
df = pd.read_csv("data/engineered_exercise_dataset.csv")
model = joblib.load("models/calories_prediction_model.pkl")

class PredictionRequest(BaseModel):
    activity: str
    weight_lbs: float
    duration_minutes: int

@app.post("/predict")
def predict(request: PredictionRequest):
    activity_data = df[df['activity'] == request.activity].iloc[0]
    met = activity_data['estimated_met']
    calories_per_kg = activity_data['Calories per kg']
    
    # Feature engineering
    weight_ratios = {w: w / request.weight_lbs for w in [130, 155, 180, 205]}
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
    
    calories_per_hour = float(model.predict(input_data)[0])
    total_calories = calories_per_hour * request.duration_minutes / 60
    
    return {
        "activity": request.activity,
        "weight_lbs": request.weight_lbs,
        "duration_minutes": request.duration_minutes,
        "calories_per_hour": round(calories_per_hour, 2),
        "total_calories": round(total_calories, 2),
        "intensity": activity_data['intensity'],
        "met": round(met, 1)
    }
```

**Run API Server**:
```bash
pip install fastapi uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Test API**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "activity": "Running",
    "weight_lbs": 170,
    "duration_minutes": 30
  }'
```

---

## Environment Variables

For advanced configurations, create `.env` file:

```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true
```

Load in app:
```python
import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv('STREAMLIT_SERVER_PORT', 8501)
```

---

## Monitoring & Maintenance

### Health Checks
- Visit deployed URL weekly
- Verify model predictions are reasonable
- Check data file freshness
- Monitor for errors in logs

### Regular Updates
- Update dependencies monthly
- Monitor for security patches
- Test on new Python versions (annually)
- Review and optimize performance

### Backup Strategy
- Keep local backup of model
- Version control all data
- Archive old deployments
- Document any changes

---

## Production Checklist

Before deploying to production:

- [ ] Python 3.11+ environment configured
- [ ] All dependencies in requirements.txt
- [ ] Error handling tested
- [ ] Data files validated and versioned
- [ ] Model performance confirmed
- [ ] Security measures in place (input validation)
- [ ] Logging enabled and tested
- [ ] Documentation updated
- [ ] Deployment tested locally first
- [ ] Rollback plan in place

---

## Support & Troubleshooting

### Check Logs
**Streamlit Cloud**: View in deployment settings
**Local**: Check terminal output
**Docker**: `docker logs container-id`

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| App crashes on startup | Check requirements match installed versions |
| Slow predictions | Clear Streamlit cache: `streamlit cache clear` |
| Model errors | Verify model file integrity: `joblib.load(path)` |
| Data not loading | Check file paths are relative to repo root |
| Port conflicts | Use different port: `--server.port 8502` |

---

## Performance Expectations

| Metric | Expected | Maximum |
|--------|----------|---------|
| App startup | <2s | 5s |
| Prediction | <50ms | 100ms |
| Page response | <100ms | 200ms |
| Concurrent users | 50+ | 100+ |
| Memory usage | <500MB | <1GB |

---

## Next Steps

1. **Deploy**: Push to Streamlit Cloud or use Docker
2. **Monitor**: Check performance regularly
3. **Update**: Keep dependencies current
4. **Extend**: Add features or integrate with other apps

For integration guidance, see [INTEGRATION.md](docs/INTEGRATION.md)
