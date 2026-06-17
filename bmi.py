"""
BMI Calculation Module
Handles BMI calculation and category determination
"""

from constants import BMI_CATEGORIES, DEFAULT_CATEGORY


def validate_positive(value, name):
    """Raise ValueError if value is not positive."""
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0")


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
    validate_positive(height, "Height")
    validate_positive(weight, "Weight")

    bmi = weight / (height ** 2)
    return round(bmi, 1)


def get_bmi_category(bmi):
    """
    Determine BMI category based on BMI value using thresholds
    defined in constants.BMI_CATEGORIES.

    Args:
        bmi (float): BMI value

    Returns:
        str: BMI category
    """
    for name, lo, hi in BMI_CATEGORIES:
        if lo <= bmi < hi:
            return name
    return DEFAULT_CATEGORY
