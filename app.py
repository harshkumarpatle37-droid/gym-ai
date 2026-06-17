"""
FitBot - Gym Assistant Chatbot
Main application file using Streamlit
"""

import streamlit as st

from bmi import calculate_bmi, get_bmi_category
from constants import get_bmi_category_labels
from db import init_database, save_user_data, get_recent_users
from workout import get_workout_plan
from diet import get_diet_plan

# Page configuration
st.set_page_config(
    page_title="FitBot - Your Gym Assistant",
    page_icon="💪",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def render_result_card(title, content):
    """Render a styled result card with the given title and markdown content."""
    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f"### {title}")
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)


_ST_ALERT = {
    "warning": st.warning,
    "info": st.info,
    "success": st.success,
    "error": st.error,
}

BMI_DISPLAY_STYLES = {
    "Underweight": ("warning", "info"),
    "Normal Weight": ("success", "success"),
    "Overweight": ("warning", "warning"),
}
BMI_DISPLAY_DEFAULT = ("error", "error")


def display_bmi_result(bmi, bmi_category):
    """Display color-coded BMI score and category."""
    score_style, cat_style = BMI_DISPLAY_STYLES.get(bmi_category, BMI_DISPLAY_DEFAULT)
    _ST_ALERT[score_style](f"**BMI Score:** {bmi:.1f}")
    _ST_ALERT[cat_style](f"**Category:** {bmi_category}")


def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1 style="color: white;">💪 FitBot - Your Personal Gym Assistant</h1>
            <p style="color: white;">Get personalized workout and diet recommendations</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize database
    if not init_database():
        st.error("Database connection error. Please try again.")
        st.stop()

    # Create two columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📝 Enter Your Details")

        # User input form
        with st.form("user_info_form"):
            name = st.text_input("Full Name", placeholder="Enter your name")
            age = st.number_input("Age", min_value=10, max_value=100, step=1,
                                 help="Age must be between 10 and 100")
            height = st.number_input("Height (cm)", min_value=0.0, step=0.1,
                                    help="Enter height in centimeters")
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1,
                                    help="Enter weight in kilograms")

            # Calculate button
            submitted = st.form_submit_button("Calculate My BMI & Get Plan", use_container_width=True)

    # Validation and processing
    if submitted:
        # Input validation
        errors = []

        if not name.strip():
            errors.append("Please enter your name")

        if age < 10 or age > 100:
            errors.append("Age must be between 10 and 100 years")

        if height <= 0:
            errors.append("Height must be greater than 0")

        if weight <= 0:
            errors.append("Weight must be greater than 0")

        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Convert height from cm to meters
            height_meters = height / 100

            # Calculate BMI
            bmi = calculate_bmi(weight, height_meters)
            bmi_category = get_bmi_category(bmi)

            # Get recommendations
            workout_plan = get_workout_plan(bmi_category)
            diet_plan = get_diet_plan(bmi_category)

            # Save to database
            if save_user_data(name, age, height, weight, bmi, bmi_category):
                st.success("✅ Your data has been saved successfully!")

                # Display results in second column
                with col2:
                    st.markdown("### 📊 Your Results")

                    # BMI Card
                    with st.container():
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        display_bmi_result(bmi, bmi_category)
                        st.markdown('</div>', unsafe_allow_html=True)

                    render_result_card("🏋️‍♂️ Recommended Workout Plan", workout_plan)
                    render_result_card("🥗 Recommended Diet Plan", diet_plan)

                    # Motivational message
                    st.balloons()
                    st.info("💡 **Pro Tip:** Consistency is key! Stick to your plan for best results.")
            else:
                st.error("Failed to save data. Please try again.")

    # Sidebar with additional info
    with st.sidebar:
        st.markdown("### 📊 BMI Categories")
        category_labels = get_bmi_category_labels()
        st.markdown("\n".join(f"- {label}" for label in category_labels))

        st.markdown("---")
        st.markdown("### 💡 Tips for Success")
        st.markdown("""
        ✅ Stay hydrated\n
        ✅ Get adequate sleep\n
        ✅ Be consistent\n
        ✅ Track your progress\n
        ✅ Listen to your body
        """)

        # Show recent users
        st.markdown("---")
        st.markdown("### 📈 Recent Users")
        recent_users = get_recent_users()
        if recent_users is not None and not recent_users.empty:
            st.dataframe(recent_users, use_container_width=True)
        else:
            st.info("No users yet. Be the first!")

if __name__ == "__main__":
    main()
