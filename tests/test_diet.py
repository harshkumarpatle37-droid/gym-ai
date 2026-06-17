"""Tests for the diet recommendation module."""

import pytest
from diet import get_diet_plan


class TestGetDietPlan:
    """Tests for get_diet_plan function."""

    def test_underweight_plan_returned(self):
        plan = get_diet_plan("Underweight")
        assert plan is not None
        assert len(plan) > 0

    def test_underweight_plan_content(self):
        plan = get_diet_plan("Underweight")
        assert "High Calorie" in plan
        assert "Protein" in plan
        assert "Eggs" in plan
        assert "Breakfast" in plan

    def test_normal_weight_plan_returned(self):
        plan = get_diet_plan("Normal Weight")
        assert plan is not None
        assert len(plan) > 0

    def test_normal_weight_plan_content(self):
        plan = get_diet_plan("Normal Weight")
        assert "Balanced" in plan
        assert "fruits and vegetables" in plan
        assert "Breakfast" in plan

    def test_overweight_plan_returned(self):
        plan = get_diet_plan("Overweight")
        assert plan is not None
        assert len(plan) > 0

    def test_overweight_plan_content(self):
        plan = get_diet_plan("Overweight")
        assert "Low Calorie" in plan
        assert "Leafy greens" in plan
        assert "Foods to Avoid" in plan

    def test_obese_plan_returned(self):
        plan = get_diet_plan("Obese")
        assert plan is not None
        assert len(plan) > 0

    def test_obese_plan_content(self):
        plan = get_diet_plan("Obese")
        assert "Controlled" in plan
        assert "portion sizes" in plan
        assert "water" in plan.lower()

    def test_unknown_category_falls_back_to_normal(self):
        plan = get_diet_plan("Unknown")
        normal_plan = get_diet_plan("Normal Weight")
        assert plan == normal_plan

    def test_empty_category_falls_back_to_normal(self):
        plan = get_diet_plan("")
        normal_plan = get_diet_plan("Normal Weight")
        assert plan == normal_plan

    def test_case_sensitive_lookup(self):
        plan = get_diet_plan("underweight")
        normal_plan = get_diet_plan("Normal Weight")
        # lowercase "underweight" is not a valid key, should fall back
        assert plan == normal_plan

    def test_return_type_is_string(self):
        plan = get_diet_plan("Underweight")
        assert isinstance(plan, str)

    def test_all_plans_contain_meal_plan(self):
        for category in ["Underweight", "Normal Weight", "Overweight", "Obese"]:
            plan = get_diet_plan(category)
            assert "Breakfast" in plan
            assert "Lunch" in plan
            assert "Dinner" in plan

    def test_all_plans_are_distinct(self):
        categories = ["Underweight", "Normal Weight", "Overweight", "Obese"]
        plans = [get_diet_plan(c) for c in categories]
        # Each plan should be unique
        assert len(set(plans)) == len(plans)

    def test_obese_plan_uses_obese_key(self):
        """The function has a special case for Obese that returns diet_plans['Obese']."""
        plan = get_diet_plan("Obese")
        assert "Controlled" in plan
        assert "Nutrient-Dense" in plan
