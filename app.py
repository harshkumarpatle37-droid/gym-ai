"""
FitBot - Gym Assistant Chatbot
Main application file using Streamlit
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from bmi import calculate_bmi, get_bmi_category
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

def init_database():
    """Initialize SQLite database and create table if not exists"""
    try:
        conn = sqlite3.connect('gym.db')
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                bmi REAL NOT NULL,
                bmi_category TEXT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return False

def save_user_data(name, age, height, weight, bmi, bmi_category):
    """Save user data to database"""
    try:
        conn = sqlite3.connect('gym.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, age, height, weight, bmi, bmi_category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, height, weight, bmi, bmi_category))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

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
                        
                        # Display BMI with color coding
                        if bmi_category == "Underweight":
                            st.warning(f"**BMI Score:** {bmi:.1f}")
                            st.info(f"**Category:** {bmi_category}")
                        elif bmi_category == "Normal Weight":
                            st.success(f"**BMI Score:** {bmi:.1f}")
                            st.success(f"**Category:** {bmi_category}")
                        elif bmi_category == "Overweight":
                            st.warning(f"**BMI Score:** {bmi:.1f}")
                            st.warning(f"**Category:** {bmi_category}")
                        else:
                            st.error(f"**BMI Score:** {bmi:.1f}")
                            st.error(f"**Category:** {bmi_category}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Workout Plan Card
                    with st.container():
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown("### 🏋️‍♂️ Recommended Workout Plan")
                        st.markdown(workout_plan)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Diet Plan Card
                    with st.container():
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown("### 🥗 Recommended Diet Plan")
                        st.markdown(diet_plan)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Motivational message
                    st.balloons()
                    st.info("💡 **Pro Tip:** Consistency is key! Stick to your plan for best results.")
            else:
                st.error("Failed to save data. Please try again.")
    
    # Sidebar with additional info
    with st.sidebar:
        st.markdown("### 📊 BMI Categories")
        st.markdown("""
        - **Underweight:** < 18.5
        - **Normal Weight:** 18.5 - 24.9
        - **Overweight:** 25 - 29.9
        - **Obese:** 30+
        """)
        
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
        try:
            conn = sqlite3.connect('gym.db')
            recent_users = pd.read_sql_query("SELECT name, bmi, bmi_category FROM users ORDER BY id DESC LIMIT 5", conn)
            conn.close()
            
            if not recent_users.empty:
                st.dataframe(recent_users, use_container_width=True)
            else:
                st.info("No users yet. Be the first!")
        except:
            st.info("Unable to load recent users")

if __name__ == "__main__":
    main()