"""
Test suite for MetriBurn utility functions
"""
import pytest
import numpy as np
from utilities.shared_utils import (
    validate_calorie_input, 
    calculate_calorie_metrics, 
    get_food_equivalents,
    format_duration_display
)

def test_validate_calorie_input_valid():
    """Test validation with valid calorie input data"""
    valid_data = {
        'weight': 70.0,
        'duration': 30,
        'activity': 'Running'
    }
    
    is_valid, message = validate_calorie_input(valid_data)
    assert is_valid == True
    assert "Valid input data" in message

def test_validate_calorie_input_invalid_weight():
    """Test validation with invalid weight"""
    invalid_data = {
        'weight': 500,  # Too high
        'duration': 30,
        'activity': 'Running'
    }
    
    is_valid, message = validate_calorie_input(invalid_data)
    assert is_valid == False
    assert "Invalid value for weight" in message

def test_validate_calorie_input_missing_fields():
    """Test validation with missing required fields"""
    incomplete_data = {
        'weight': 70.0,
        'duration': 30
        # Missing 'activity'
    }
    
    is_valid, message = validate_calorie_input(incomplete_data)
    assert is_valid == False
    assert "Missing required fields" in message

def test_calculate_calorie_metrics():
    """Test calorie metrics calculation"""
    calories_burned = 300.0
    weight = 70.0
    duration = 30.0
    
    metrics = calculate_calorie_metrics(calories_burned, weight, duration)
    
    assert metrics['total_calories'] == 300.0
    assert metrics['calories_per_minute'] == 10.0  # 300/30
    assert metrics['calories_per_kg'] == pytest.approx(4.29, rel=1e-2)  # 300/70
    assert metrics['met_estimate'] > 0
    assert metrics['intensity_level'] in ['Light', 'Moderate', 'Vigorous']

def test_calculate_calorie_metrics_edge_cases():
    """Test metrics calculation with edge cases"""
    # Test with zero duration (should not crash)
    metrics = calculate_calorie_metrics(100.0, 70.0, 0.0)
    assert metrics['calories_per_minute'] == 100.0  # 100/max(0,1) = 100
    
    # Test with zero weight (should not crash)
    metrics = calculate_calorie_metrics(100.0, 0.0, 30.0)
    assert metrics['calories_per_kg'] == 100.0  # 100/max(0,1) = 100

def test_get_food_equivalents():
    """Test food equivalent calculations"""
    calories = 285  # Exactly one slice of pizza
    
    equivalents = get_food_equivalents(calories)
    
    # Should find pizza equivalent
    pizza_equiv = next((item for item in equivalents if item['food'] == 'Slice of Pizza'), None)
    assert pizza_equiv is not None
    assert float(pizza_equiv['quantity']) == pytest.approx(1.0, rel=1e-1)
    
    # Should have multiple food options
    assert len(equivalents) >= 3

def test_get_food_equivalents_small_calories():
    """Test food equivalents with small calorie amounts"""
    calories = 50  # Small amount
    
    equivalents = get_food_equivalents(calories)
    
    # Should only show items where quantity >= 0.5
    for equiv in equivalents:
        assert float(equiv['quantity']) >= 0.5

def test_format_duration_display():
    """Test duration formatting"""
    # Test minutes only
    assert format_duration_display(30) == "30 minutes"
    assert format_duration_display(45) == "45 minutes"
    
    # Test hours only
    assert format_duration_display(60) == "1 hour"
    assert format_duration_display(120) == "2 hours"
    
    # Test hours and minutes
    assert format_duration_display(90) == "1h 30m"
    assert format_duration_display(135) == "2h 15m"

def test_format_duration_display_edge_cases():
    """Test duration formatting with edge cases"""
    # Test zero and small values
    assert format_duration_display(0) == "0 minutes"
    assert format_duration_display(1) == "1 minutes"
    
    # Test large values
    assert format_duration_display(300) == "5 hours"
    assert format_duration_display(305) == "5h 5m"