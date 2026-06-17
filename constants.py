"""
Shared constants for the FitBot application.
Centralizes BMI category definitions and configuration so they are defined once.
"""

DB_PATH = "gym.db"

DEFAULT_CATEGORY = "Normal Weight"

# Ordered list of (category_name, min_bmi, max_bmi) tuples.
# max_bmi is exclusive for all but the last entry (which is unbounded).
BMI_CATEGORIES = [
    ("Underweight", 0, 18.5),
    ("Normal Weight", 18.5, 25.0),
    ("Overweight", 25.0, 30.0),
    ("Obese", 30.0, float("inf")),
]


def get_bmi_category_labels():
    """Return a list of human-readable BMI category descriptions for display."""
    labels = []
    for name, lo, hi in BMI_CATEGORIES:
        if hi == float("inf"):
            labels.append(f"**{name}:** {lo}+")
        else:
            labels.append(f"**{name}:** {lo} - {hi - 0.1}")
    return labels


def get_plan_by_category(plans, bmi_category):
    """Look up a plan dict by BMI category, falling back to DEFAULT_CATEGORY."""
    return plans.get(bmi_category, plans[DEFAULT_CATEGORY])
