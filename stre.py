import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="College Courses Dashboard",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# Load data
df = pd.read_csv('data/CollegeCourseList.csv')

# Filter out specific university
df_filtered = df[df['University'] != "MAHARASHTRA STATE BOARD OF SECONDARY AND HIGHER SECONDARY EDUCATION"]

# Remove duplicates for dropdowns
unique_universities = df_filtered['University'].unique()
unique_course_categories = df_filtered['Course Category'].unique()

# Sidebar - Selection boxes
st.sidebar.header('Filter') 

# Dropdown to select University
selected_university = st.sidebar.selectbox('University', unique_universities)

# Dropdown to select Course Category
selected_course_category = st.sidebar.selectbox('Course Category', unique_course_categories)

# Filtering data based on selection
df_display = df_filtered[(df_filtered['University'] == selected_university) & (df_filtered['Course Category'] == selected_course_category)]

# Display filtered dataframe
st.write(df_display)
