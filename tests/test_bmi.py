"""Tests for the BMI calculation module."""

import pytest
from bmi import calculate_bmi, get_bmi_category


class TestCalculateBmi:
    """Tests for calculate_bmi function."""

    def test_normal_bmi(self):
        # 70 kg, 1.75 m -> 70 / 3.0625 = 22.9
        assert calculate_bmi(70, 1.75) == 22.9

    def test_underweight_bmi(self):
        # 50 kg, 1.80 m -> 50 / 3.24 = 15.4
        assert calculate_bmi(50, 1.80) == 15.4

    def test_overweight_bmi(self):
        # 85 kg, 1.70 m -> 85 / 2.89 = 29.4
        assert calculate_bmi(85, 1.70) == 29.4

    def test_obese_bmi(self):
        # 110 kg, 1.70 m -> 110 / 2.89 = 38.1
        assert calculate_bmi(110, 1.70) == 38.1

    def test_result_rounded_to_one_decimal(self):
        # 68 kg, 1.73 m -> 68 / 2.9929 = 22.7196... -> 22.7
        result = calculate_bmi(68, 1.73)
        assert result == round(result, 1)

    def test_very_light_person(self):
        result = calculate_bmi(30, 1.50)
        assert result == 13.3

    def test_very_heavy_person(self):
        result = calculate_bmi(200, 1.80)
        assert result == 61.7

    def test_short_height(self):
        result = calculate_bmi(60, 1.20)
        assert result == 41.7

    def test_tall_height(self):
        result = calculate_bmi(80, 2.10)
        assert result == 18.1

    def test_zero_height_raises_error(self):
        with pytest.raises(ValueError, match="Height must be greater than 0"):
            calculate_bmi(70, 0)

    def test_negative_height_raises_error(self):
        with pytest.raises(ValueError, match="Height must be greater than 0"):
            calculate_bmi(70, -1.75)

    def test_zero_weight_raises_error(self):
        with pytest.raises(ValueError, match="Weight must be greater than 0"):
            calculate_bmi(0, 1.75)

    def test_negative_weight_raises_error(self):
        with pytest.raises(ValueError, match="Weight must be greater than 0"):
            calculate_bmi(-70, 1.75)

    def test_both_zero_raises_error(self):
        with pytest.raises(ValueError):
            calculate_bmi(0, 0)

    def test_small_positive_values(self):
        result = calculate_bmi(0.1, 0.1)
        assert result == 10.0

    def test_return_type_is_float(self):
        result = calculate_bmi(70, 1.75)
        assert isinstance(result, float)


class TestGetBmiCategory:
    """Tests for get_bmi_category function."""

    def test_underweight(self):
        assert get_bmi_category(15.0) == "Underweight"

    def test_underweight_boundary_below(self):
        assert get_bmi_category(18.4) == "Underweight"

    def test_normal_weight_lower_boundary(self):
        assert get_bmi_category(18.5) == "Normal Weight"

    def test_normal_weight_middle(self):
        assert get_bmi_category(22.0) == "Normal Weight"

    def test_normal_weight_upper_boundary(self):
        assert get_bmi_category(24.9) == "Normal Weight"

    def test_overweight_lower_boundary(self):
        assert get_bmi_category(25.0) == "Overweight"

    def test_overweight_middle(self):
        assert get_bmi_category(27.5) == "Overweight"

    def test_overweight_upper_boundary(self):
        assert get_bmi_category(29.9) == "Overweight"

    def test_obese_lower_boundary(self):
        assert get_bmi_category(30.0) == "Obese"

    def test_obese_high_value(self):
        assert get_bmi_category(45.0) == "Obese"

    def test_very_low_bmi(self):
        assert get_bmi_category(10.0) == "Underweight"

    def test_very_high_bmi(self):
        assert get_bmi_category(60.0) == "Obese"

    def test_return_type_is_string(self):
        result = get_bmi_category(22.0)
        assert isinstance(result, str)
