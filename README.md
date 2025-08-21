# 🔥 MetriBurn - AI-Powered Calorie Prediction Platform

[![CI/CD Pipeline](https://github.com/dkumi12/CaloriesBurnt/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/dkumi12/CaloriesBurnt/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

> **Professional machine learning platform for predicting calories burned during physical activities with 1,248+ exercise database and food equivalent visualizations**

**Powered by Ever Booming Health and Wellness®**

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dkumi12/CaloriesBurnt/main/metriburn_app.py)

## ✨ Core Features

### **AI-Powered Predictions**
- **🤖 Machine Learning Model**: Advanced regression model for accurate calorie estimation
- **📊 1,248+ Activities**: Comprehensive exercise database covering all activity types
- **⚖️ Personalized Results**: Predictions based on individual weight and exercise duration
- **🍎 Food Equivalents**: Visual representations using familiar food items

### **Professional Engineering**
- **✅ Comprehensive Testing**: Full test suite with 9 comprehensive tests
- **✅ Input Validation**: Professional data validation and error handling
- **✅ Shared Utilities**: Clean, maintainable code architecture
- **✅ CI/CD Pipeline**: Automated testing and quality assurance
- **✅ Performance Optimized**: Fast predictions with cached models
- **✅ User Experience**: Professional Streamlit interface with dark theme

### **Health & Wellness Focus**
- **🎯 Fitness Goals**: Support for various fitness and weight management goals
- **📈 Metabolic Insights**: MET calculations and exercise intensity classification
- **🏃‍♀️ Activity Tracking**: Wide range of activities from walking to competitive sports
- **🔍 Detailed Analytics**: Calories per minute, per kg, and intensity metrics

## 🛠️ Technology Stack

### **Machine Learning**
- **Python 3.11+** - Modern Python with latest features
- **Scikit-learn** - Professional ML model implementation
- **Pandas & NumPy** - Data processing and numerical computations
- **Joblib** - Model persistence and loading

### **Web Application**
- **Streamlit** - Interactive web application framework
- **Professional UI** - Custom CSS with dark theme and branding
- **Responsive Design** - Mobile-friendly interface
- **PWA Ready** - Progressive web app capabilities

### **Development & Quality**
- **Pytest** - Comprehensive testing framework
- **GitHub Actions** - CI/CD pipeline with automated testing
- **Code Quality** - Linting, formatting, and security scanning
- **Professional Documentation** - Complete guides and API documentation

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11 or higher
- Git

### **Installation**
```bash
# Clone the repository
git clone https://github.com/dkumi12/CaloriesBurnt.git
cd CaloriesBurnt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run metriburn_app.py
```

### **Usage**
1. **Access the app**: Open http://localhost:8501 in your browser
2. **Select activity**: Choose from 1,248+ available exercises
3. **Enter details**: Input your weight and exercise duration
4. **Get prediction**: Receive accurate calorie burn estimation
5. **View insights**: See MET values, intensity levels, and food equivalents

## 📁 Project Structure

```
MetriBurn/
├── metriburn_app.py          # Main Streamlit application
├── utilities/                # Shared utility functions
│   ├── shared_utils.py      # Professional utilities and validation
│   ├── create_sample_data.py # Data preparation utilities
│   └── [analysis tools]     # Additional utility scripts
├── tests/                    # Comprehensive test suite
│   ├── test_shared_utils.py # Utility function tests (9 tests)
│   └── __init__.py          # Test package initialization
├── data/                     # Dataset storage
├── models/                   # Trained ML models
├── static/                   # Web assets and styling
├── .github/workflows/        # CI/CD automation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## 🧪 Testing & Validation

### **Test Suite Results**
```bash
# Run comprehensive test suite
pytest tests/ -v

# Expected output:
tests/test_shared_utils.py::test_validate_calorie_input_valid PASSED
tests/test_shared_utils.py::test_validate_calorie_input_invalid_weight PASSED  
tests/test_shared_utils.py::test_validate_calorie_input_missing_fields PASSED
tests/test_shared_utils.py::test_calculate_calorie_metrics PASSED
tests/test_shared_utils.py::test_calculate_calorie_metrics_edge_cases PASSED
tests/test_shared_utils.py::test_get_food_equivalents PASSED
tests/test_shared_utils.py::test_get_food_equivalents_small_calories PASSED
tests/test_shared_utils.py::test_format_duration_display PASSED
tests/test_shared_utils.py::test_format_duration_display_edge_cases PASSED

9 passed in 0.94s (100% success rate)
```

### **Validation Features**
- **Input Validation**: Weight (30-300kg), Duration (1-480min), Activity (non-empty)
- **Error Handling**: Graceful handling of edge cases and invalid inputs
- **Metrics Calculation**: MET estimation, intensity classification, food equivalents
- **Performance Testing**: Fast response times with optimized calculations

## 📊 Model Information

### **Machine Learning Pipeline**
- **Algorithm**: Advanced regression model optimized for calorie prediction
- **Training Data**: Comprehensive exercise database with metabolic data
- **Features**: Activity type, user weight, exercise duration, intensity factors
- **Validation**: Cross-validated performance with real-world activity data

### **Prediction Accuracy**
- **Exercise Coverage**: 1,248+ different physical activities
- **Weight Range**: Supports 30kg to 300kg (66-660 lbs)
- **Duration Range**: 1 minute to 8 hours of exercise
- **Accuracy**: Validated against metabolic equivalent databases

## 🎨 User Interface

### **Professional Design**
- **Dark Theme**: Eye-friendly interface with professional styling
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Interactive Elements**: Smooth animations and user feedback
- **Accessibility**: Screen reader compatible with proper ARIA labels

### **User Experience Features**
- **Smart Search**: Easy activity selection with categorization
- **Visual Feedback**: Real-time calorie calculations and updates
- **Food Equivalents**: Relatable comparisons (apples, pizza slices, etc.)
- **Intensity Indicators**: MET-based exercise intensity classification

## 🔒 Security & Privacy

### **Data Protection**
- **No Personal Storage**: User data processed locally, not stored
- **Input Validation**: Comprehensive sanitization of all user inputs
- **Error Handling**: Secure error management preventing data exposure
- **Privacy First**: No tracking or personal information collection

### **Security Features**
- **Input Sanitization**: Validation of all parameters and ranges
- **Error Logging**: Secure logging without personal information
- **Dependency Scanning**: Automated vulnerability detection
- **Safe Defaults**: Graceful fallbacks for edge cases

## 🚀 Deployment

### **Local Development**
```bash
streamlit run metriburn_app.py --server.runOnSave true
```

### **Production Deployment**
- **Streamlit Cloud**: Automatic deployment from GitHub
- **Environment**: Python 3.11+ with optimized dependencies
- **Performance**: Fast loading with cached models and efficient processing

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Add comprehensive tests** for new functionality
4. **Run the test suite** (`pytest tests/`)
5. **Update documentation** as needed
6. **Commit changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### **Development Standards**
- **Python**: Follow PEP 8 style guidelines
- **Testing**: Maintain >90% code coverage
- **Documentation**: Document all public functions
- **Security**: Follow secure coding practices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ever Booming Health and Wellness®** - Project sponsor and health expertise
- **Streamlit Team** - Excellent web application framework
- **Scikit-learn Community** - Machine learning tools and algorithms
- **Health Research Community** - Metabolic and exercise science data

---

<div align="center">

**Empowering fitness journeys through intelligent calorie tracking** 💪

[![GitHub stars](https://img.shields.io/github/stars/dkumi12/CaloriesBurnt.svg?style=social&label=Star)](https://github.com/dkumi12/CaloriesBurnt)

</div>