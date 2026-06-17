"""
Workout Recommendation Module
Provides workout plans based on BMI category
"""

import logging

logger = logging.getLogger(__name__)

def get_workout_plan(bmi_category):
    """
    Get workout recommendations based on BMI category
    
    Args:
        bmi_category (str): BMI category (Underweight, Normal Weight, Overweight, Obese)
    
    Returns:
        str: Formatted workout plan with recommendations
    
    Raises:
        ValueError: If bmi_category is not a recognized category
    """
    
    workout_plans = {
        "Underweight": """
        🏋️‍♂️ **Strength Training Focus**\n
        • Push-ups: 3 sets of 8-12 reps
        • Squats: 3 sets of 10-15 reps
        • Pull-ups or Lat pulldowns: 3 sets of 6-10 reps
        • Dumbbell rows: 3 sets of 10-12 reps
        • Planks: 3 sets of 20-30 seconds\n
        📅 **Frequency:** 4-5 days per week
        ⏱️ **Duration:** 45-60 minutes per session
        """,
        
        "Normal Weight": """
        🏃‍♀️ **Balanced Fitness Program**\n
        • Jogging/Running: 20-30 minutes
        • Cardio exercises: Jumping jacks, mountain climbers
        • Full body workout: Burpees, lunges, push-ups
        • Core training: Crunches, leg raises, Russian twists
        • Stretching: 10 minutes post-workout\n
        📅 **Frequency:** 3-4 days per week
        ⏱️ **Duration:** 30-45 minutes per session
        """,
        
        "Overweight": """
        🚶‍♂️ **Fat Burning Program**\n
        • Brisk walking: 30-40 minutes daily
        • Cycling: 20-30 minutes (moderate intensity)
        • Swimming: 30 minutes (if available)
        • HIIT workouts: 15-20 minutes (beginner friendly)
        • Low impact cardio: Elliptical, rowing machine\n
        📅 **Frequency:** 5-6 days per week
        ⏱️ **Duration:** 40-50 minutes per session
        """,
        
        "Obese": """
        🏊‍♀️ **Beginner Friendly Program**\n
        • Walking: Start with 15-20 minutes daily
        • Water aerobics: Low impact on joints
        • Seated exercises: Chair cardio, arm raises
        • Gentle yoga: 15-20 minutes
        • Stationary cycling: Low intensity\n
        📅 **Frequency:** 5-6 days per week (start slow)
        ⏱️ **Duration:** 20-30 minutes, gradually increase
        ⚠️ **Important:** Consult doctor before starting
        """
    }
    
    if bmi_category not in workout_plans:
        raise ValueError(
            f"Unknown BMI category '{bmi_category}'. "
            f"Expected one of: {', '.join(workout_plans)}"
        )
    return workout_plans[bmi_category]