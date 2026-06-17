"""
BMI Calculation Module
Handles BMI calculation and category determination
"""

def calculate_bmi(weight, height):
    """
    Calculate BMI using weight (kg) and height (m)
    
    Formula: BMI = weight(kg) / height(m)^2
    
    Args:
        weight (float): Weight in kilograms
        height (float): Height in meters
    
    Returns:
        float: Calculated BMI value rounded to 1 decimal place
    """
    if height <= 0:
        raise ValueError("Height must be greater than 0")
    
    if weight <= 0:
        raise ValueError("Weight must be greater than 0")
    
    bmi = weight / (height ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """
    Determine BMI category based on BMI value
    
    Categories:
    - Underweight: < 18.5
    - Normal Weight: 18.5 - 24.9
    - Overweight: 25 - 29.9
    - Obese: 30+
    
    Args:
        bmi (float): BMI value
    
    Returns:
        str: BMI category
    
    Raises:
        TypeError: If bmi is not a number
        ValueError: If bmi is negative
    """
    if not isinstance(bmi, (int, float)):
        raise TypeError(f"BMI must be a number, got {type(bmi).__name__}")
    if bmi < 0:
        raise ValueError(f"BMI cannot be negative, got {bmi}")

    if bmi < 18.5:
        return "Underweight"
    elif bmi <= 24.9:
        return "Normal Weight"
    elif bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"