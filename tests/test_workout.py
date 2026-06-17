"""Tests for the workout recommendation module."""

import pytest
from workout import get_workout_plan


class TestGetWorkoutPlan:
    """Tests for get_workout_plan function."""

    def test_underweight_plan_returned(self):
        plan = get_workout_plan("Underweight")
        assert plan is not None
        assert len(plan) > 0

    def test_underweight_plan_content(self):
        plan = get_workout_plan("Underweight")
        assert "Strength Training" in plan
        assert "Push-ups" in plan
        assert "Squats" in plan

    def test_underweight_plan_frequency(self):
        plan = get_workout_plan("Underweight")
        assert "4-5 days per week" in plan
        assert "45-60 minutes" in plan

    def test_normal_weight_plan_returned(self):
        plan = get_workout_plan("Normal Weight")
        assert plan is not None
        assert len(plan) > 0

    def test_normal_weight_plan_content(self):
        plan = get_workout_plan("Normal Weight")
        assert "Balanced Fitness" in plan
        assert "Jogging" in plan or "Running" in plan
        assert "Core training" in plan

    def test_normal_weight_plan_frequency(self):
        plan = get_workout_plan("Normal Weight")
        assert "3-4 days per week" in plan
        assert "30-45 minutes" in plan

    def test_overweight_plan_returned(self):
        plan = get_workout_plan("Overweight")
        assert plan is not None
        assert len(plan) > 0

    def test_overweight_plan_content(self):
        plan = get_workout_plan("Overweight")
        assert "Fat Burning" in plan
        assert "Brisk walking" in plan
        assert "Cycling" in plan

    def test_overweight_plan_frequency(self):
        plan = get_workout_plan("Overweight")
        assert "5-6 days per week" in plan
        assert "40-50 minutes" in plan

    def test_obese_plan_returned(self):
        plan = get_workout_plan("Obese")
        assert plan is not None
        assert len(plan) > 0

    def test_obese_plan_content(self):
        plan = get_workout_plan("Obese")
        assert "Beginner Friendly" in plan
        assert "Walking" in plan
        assert "Consult doctor" in plan

    def test_obese_plan_frequency(self):
        plan = get_workout_plan("Obese")
        assert "5-6 days per week" in plan
        assert "20-30 minutes" in plan

    def test_unknown_category_falls_back_to_normal(self):
        plan = get_workout_plan("Unknown")
        normal_plan = get_workout_plan("Normal Weight")
        assert plan == normal_plan

    def test_empty_category_falls_back_to_normal(self):
        plan = get_workout_plan("")
        normal_plan = get_workout_plan("Normal Weight")
        assert plan == normal_plan

    def test_case_sensitive_lookup(self):
        plan = get_workout_plan("obese")
        normal_plan = get_workout_plan("Normal Weight")
        assert plan == normal_plan

    def test_return_type_is_string(self):
        plan = get_workout_plan("Underweight")
        assert isinstance(plan, str)

    def test_all_plans_are_distinct(self):
        categories = ["Underweight", "Normal Weight", "Overweight", "Obese"]
        plans = [get_workout_plan(c) for c in categories]
        assert len(set(plans)) == len(plans)

    def test_all_plans_contain_frequency(self):
        for category in ["Underweight", "Normal Weight", "Overweight", "Obese"]:
            plan = get_workout_plan(category)
            assert "Frequency" in plan
            assert "Duration" in plan
