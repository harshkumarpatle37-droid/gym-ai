"""
Diet Recommendation Module
Provides diet plans based on BMI category
"""

import logging

logger = logging.getLogger(__name__)

def get_diet_plan(bmi_category):
    """
    Get diet recommendations based on BMI category
    
    Args:
        bmi_category (str): BMI category (Underweight, Normal Weight, Overweight, Obese)
    
    Returns:
        str: Formatted diet plan with recommendations
    
    Raises:
        ValueError: If bmi_category is not a recognized category
    """
    
    diet_plans = {
        "Underweight": """
        🍽️ **High Calorie & Protein Rich Diet**\n
        **Foods to Eat:**\n
        • Whole milk and dairy products
        • Eggs (2-3 daily)
        • Nuts and dry fruits (almonds, walnuts, dates)
        • Lean meats, fish, poultry
        • Brown rice, whole wheat bread
        • Bananas, mangoes, avocados\n
        **Sample Meal Plan:**\n
        Breakfast: Oats with milk, banana, nuts
        Lunch: Brown rice with chicken/legumes
        Snack: Protein shake + dry fruits
        Dinner: Whole wheat bread with eggs/cheese
        """,
        
        "Normal Weight": """
        🥗 **Balanced & Nutritious Diet**\n
        **Foods to Eat:**\n
        • All fruits and vegetables (5 servings daily)
        • Whole grains (quinoa, brown rice, oats)
        • Lean proteins (chicken, fish, tofu, legumes)
        • Healthy fats (olive oil, nuts, seeds)
        • Probiotics (yogurt, buttermilk)\n
        **Sample Meal Plan:**\n
        Breakfast: Smoothie bowl with fruits
        Lunch: Grilled chicken salad with quinoa
        Snack: Greek yogurt + berries
        Dinner: Steamed fish with vegetables
        """,
        
        "Overweight": """
        🥬 **Low Calorie & High Fiber Diet**\n
        **Foods to Eat:**\n
        • Leafy greens (spinach, kale, lettuce)
        • Lean proteins (chicken breast, fish, tofu)
        • Green vegetables (broccoli, cucumber, zucchini)
        • Whole grains in moderation
        • Green tea, detox water\n
        **Foods to Avoid:**\n
        • Sugary drinks and sweets
        • Fried and processed foods
        • White bread and refined carbs\n
        **Sample Meal Plan:**\n
        Breakfast: Vegetable omelette
        Lunch: Large salad with grilled chicken
        Snack: Apple or cucumber slices
        Dinner: Steamed vegetables with tofu
        """,
        
        "Obese": """
        🥦 **Controlled & Nutrient-Dense Diet**\n
        **Foods to Eat:**\n
        • High fiber vegetables (broccoli, cauliflower)
        • Lean proteins in small portions
        • Whole fruits (2-3 servings)
        • Legumes and beans
        • Drink 8-10 glasses of water daily\n
        **Important Guidelines:**\n
        • Control portion sizes
        • Eat slowly and mindfully
        • No eating after 8 PM
        • Avoid all processed foods
        • Limit sugar and salt intake\n
        **Sample Meal Plan:**\n
        Breakfast: Oatmeal with berries
        Lunch: Vegetable soup with lentils
        Snack: Carrot sticks with hummus
        Dinner: Baked fish with steamed greens
        """,
        
        "Extreme Obese": """
        ⚠️ **Doctor Supervised Diet Plan**\n
        **Immediate Steps:**\n
        1. Consult a registered dietitian
        2. Get a medical checkup
        3. Start with portion control\n
        **General Guidelines:**\n
        • Eat small, frequent meals (5-6 per day)
        • Include protein in every meal
        • Avoid sugar completely
        • Drink water before meals
        • Track your calorie intake\n
        **Safe Foods:**\n
        • Fresh vegetables (steamed or raw)
        • Lean proteins (small portions)
        • Whole fruits (limited quantity)
        • Herbal teas, infused water
        """
    }
    
    if bmi_category not in diet_plans:
        raise ValueError(
            f"Unknown BMI category '{bmi_category}'. "
            f"Expected one of: {', '.join(diet_plans)}"
        )
    return diet_plans[bmi_category]